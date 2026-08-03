"""
================================================================================
毛寶企業 (Maobao) 多賣場產品與競品價格每日監控系統 [教師上課教學講義版]
--------------------------------------------------------------------------------
檔案名稱：main_for_teacher.py
教學目標：
1. 掌握 Async Playwright (async_api) 與 Python asyncio 的協程 (Coroutines) 機制
2. 理解 I/O Bound 爬蟲任務中「同步 sequential」與「非同步 concurrent」高達 10 倍的效能差距
3. 學習「混合式爬取策略 (Hybrid Scraping Approach)」：
   - 高效能 API 直連 (PChome 24h) vs 瀏覽器 DOM 自動化解析 (momo, Yahoo)
4. 熟練運用 `asyncio.gather(*tasks)` 進行多維度 (品類 x 品牌 x 賣場) 的平行併發
5. 了解數據清洗 (Regex)、防爬蟲設定 (User-Agent) 與 GFM Markdown / JSON 報表匯出
================================================================================
"""

import asyncio
import json
import os
import re
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any
from playwright.async_api import async_playwright, BrowserContext, Page

# ==============================================================================
# 0. 專案全域變數設定 (Global Configurations)
# ==============================================================================
CONFIG_FILE = "products_config.json"   # 商品與賣場組態設定檔
REPORT_JSON = "price_report.json"     # 詳細數據 JSON 報表
REPORT_MD = "price_report.md"         # GFM Markdown 競品日報檔


# ==============================================================================
# 1. 賣場爬取模組 (Store Scraping Modules)
#    - 展現 3 大平台的差別化爬取策略 (API vs DOM)
# ==============================================================================

async def fetch_pchome(context: BrowserContext, keyword: str) -> Dict[str, Any]:
    """
    【賣場一：PChome 24h 購物 - API 直連模式】
    💡 教學說明：
       PChome 的搜尋頁面底層採用開放 API (ecshweb.pchome.com.tw)。
       我們不需要啟動 Page 瀏覽器分頁去渲染 HTML，直接利用 Playwright 提供的
       `context.request.get()` 發送高效率 HTTP 請求，可以直接拿到 JSON 資料！
       速度極快（僅需數毫秒），且極度節省 CPU/記憶體資源。
    """
    result = {
        "platform": "PChome 24h",
        "title": "未找到相關商品",
        "price": 0,
        "url": "",
        "status": "無結果"
    }

    # URL 關鍵字編碼 (避免中文關鍵字造成 URL 格式錯誤)
    encoded_kw = urllib.parse.quote(keyword)
    api_url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={encoded_kw}&page=1"

    try:
        # 使用 context.request 發起非同步 GET 請求
        response = await context.request.get(api_url, timeout=10000)
        if response.status == 200:
            data = await response.json()
            prods = data.get("prods", [])
            if prods:
                # 抓取搜尋結果第一筆商品
                item = prods[0]
                result["title"] = item.get("name", "未知的商品標題")
                result["price"] = int(item.get("price", 0))
                result["url"] = f"https://24h.pchome.com.tw/prod/{item.get('Id', '')}"
                result["status"] = "成功"
                return result
    except Exception as e:
        # 實務上的例外容錯，確保單一賣場失敗不會中斷整個併發任務
        pass

    return result


async def fetch_momo(context: BrowserContext, keyword: str) -> Dict[str, Any]:
    """
    【賣場二：momo 購物網 - DOM 動態解析模式】
    💡 教學說明：
       momo 採用渲染較複雜的動態網頁。這裡使用 Playwright 開啟獨立 `Page` 分頁：
       1. 使用 `wait_until="domcontentloaded"` 避免 networkidle 導致廣告追蹤請求超時。
       2. 使用 `locator()` 精準定位商品卡片、標題與價格。
       3. 使用正則表達式 `re.sub(r"[^\d]", "", price_text)` 清理價格字串（如 "NT$ 1,090" -> 1090）。
       4. 在 `finally` 區塊務必執行 `await page.close()` 釋放頁面記憶體。
    """
    result = {
        "platform": "momo購物網",
        "title": "未找到相關商品",
        "price": 0,
        "url": "",
        "status": "無結果"
    }

    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={encoded_kw}"
    
    # 建立非同步 Page 頁面
    page: Page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(1000) # 給予前端模板動態填入文字短暫緩衝
        
        # 多重選擇器防護：適應 momo 可能變更的商品卡片 CSS class
        cards = page.locator("div.listArea ul li, .prdListArea ul li")
        
        if await cards.count() > 0:
            card = cards.first
            title_loc = card.locator(".prdName, h3, .goodsName")
            price_loc = card.locator(".price, .money, .prdPrice")
            link_loc = card.locator("a.goods-img-url, a.prdName, a").first

            title = await title_loc.first.inner_text() if await title_loc.count() > 0 else ""
            price_text = await price_loc.first.inner_text() if await price_loc.count() > 0 else ""
            href = await link_loc.get_attribute("href") if await link_loc.count() > 0 else ""

            # 正則表達式數據清洗：移除所有非數字字元 (例如 $, comma, 符號)
            digits = re.sub(r"[^\d]", "", price_text)
            price = int(digits) if digits else 0

            # 補全相對路徑 URL
            if href and not href.startswith("http"):
                href = f"https://www.momoshop.com.tw{href}"

            if title:
                result["title"] = title.strip()
                result["price"] = price
                result["url"] = href
                result["status"] = "成功"
    except Exception:
        pass
    finally:
        # 關鍵！在 Playwright 併發爬蟲中，完成任務必須關閉 Page 避免記憶體洩漏 (Memory Leak)
        await page.close()

    return result


async def fetch_yahoo(context: BrowserContext, keyword: str) -> Dict[str, Any]:
    """
    【賣場三：Yahoo 購物中心 - DOM 列表分析模式】
    💡 教學說明：
       Yahoo 購物中心商品列表中混雜廣告與促銷標籤 (如 "折", "限時下殺", "找相似")。
       本函式展示如何抓取商品卡片的多行文字 (inner_text split)，並過濾無效字串找到真正標題與價格。
    """
    result = {
        "platform": "Yahoo購物中心",
        "title": "未找到相關商品",
        "price": 0,
        "url": "",
        "status": "無結果"
    }

    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://tw.buy.yahoo.com/search/product?p={encoded_kw}"
    page: Page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(1200)
        cards = page.locator("a[href*='/gdsale/']")

        if await cards.count() > 0:
            card = cards.first
            href = await card.get_attribute("href")
            txt = await card.inner_text()
            lines = [l.strip() for l in txt.split("\n") if l.strip()]

            title = ""
            price = 0
            for l in lines:
                if l.startswith("$"):
                    digits = re.sub(r"[^\d]", "", l)
                    if digits and price == 0:
                        price = int(digits)
                elif l not in ["比較", "找相似", "活動", "券", "限時下殺", "折扣"] and not title:
                    title = l

            if title:
                result["title"] = title
                result["price"] = price
                result["url"] = href or ""
                result["status"] = "成功"
    except Exception:
        pass
    finally:
        await page.close()

    return result


# ==============================================================================
# 2. 非同步平行併發核心邏輯 (Async Concurrency Logic)
#    - asyncio.gather 實現 3 層多維度併發
# ==============================================================================

async def fetch_item_across_platforms(context: BrowserContext, brand: str, name: str, keyword: str) -> Dict[str, Any]:
    """
    【併發層級 3：跨賣場平台併發】
    💡 教學說明：
       針對單一商品 (如 "毛寶 貼身衣物手洗精")，同時向 PChome、momo、Yahoo 3 個平台發起非同步任務！
       `asyncio.gather(*stores_tasks)` 會同時執行這 3 個 Coroutines，
       執行時間取決於 3 個賣場中「最慢的那一個」（約 1~2 秒），而非 3 個賣場相加（4~6 秒）！
    """
    stores_tasks = [
        fetch_pchome(context, keyword),
        fetch_momo(context, keyword),
        fetch_yahoo(context, keyword)
    ]
    # 同時等待所有賣場回傳結果
    store_results = await asyncio.gather(*stores_tasks)

    return {
        "brand": brand,
        "name": name,
        "keyword": keyword,
        "stores": store_results
    }


async def monitor_category_async(context: BrowserContext, category_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    【併發層級 2：跨品牌/競品併發】
    💡 教學說明：
       針對單一品類（如 "貼身衣物手洗精"），同時抓取「毛寶本家商品」與「多個競品品牌」。
    """
    category_name = category_item["category"]
    maobao_cfg = category_item["maobao_product"]
    competitors_cfg = category_item["competitors"]

    print(f"🚀 開始平行併發查詢品類：【{category_name}】跨賣場數據...")

    tasks = [
        fetch_item_across_platforms(context, "毛寶", maobao_cfg["name"], maobao_cfg["keyword"])
    ]
    for comp in competitors_cfg:
        tasks.append(fetch_item_across_platforms(context, comp["brand"], comp["name"], comp["keyword"]))

    # 同時執行毛寶與所有競品的抓取任務
    results = await asyncio.gather(*tasks)

    return {
        "category": category_name,
        "maobao_product": results[0],
        "competitors": results[1:]
    }


# ==============================================================================
# 3. 主程式進入點 (Main Flow)
# ==============================================================================

async def main():
    print("=" * 80)
    print("毛寶企業 (Maobao) 多賣場產品與競品價格每日監控系統 [Playwright Async版 - 教師教學用]")
    print("=" * 80)

    # 1. 檢查並讀取 JSON 組態檔 (展現組態驅動設計 Configuration-Driven)
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ 找不到設定檔：{CONFIG_FILE}")
        return

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    categories = config_data.get("monitor_products", [])
    platforms = config_data.get("platforms", [])
    platform_names = [p["name"] for p in platforms]

    print(f"📦 載入設定完成！監控 {len(categories)} 大品類，跨賣場：{', '.join(platform_names)}...\n")

    start_time = datetime.now()

    # 2. 啟動 Playwright Async 引擎與 BrowserContext (瀏覽器上下文)
    async with async_playwright() as p:
        # headless=True 以背景模式執行（可設定 headless=False 觀察瀏覽器自動化操作過程）
        browser = await p.chromium.launch(headless=True)
        
        # 建立全局 Context，注入通用 User-Agent 與 Viewport
        context: BrowserContext = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )

        # 【併發層級 1：跨品類併發】
        # 同時為 5 大品類發起非同步監控任務
        cat_tasks = [monitor_category_async(context, cat) for cat in categories]
        
        # asyncio.gather 啟動所有品類 x 品牌 x 賣場 的超大規模平行併發！
        all_results = await asyncio.gather(*cat_tasks)

        # 釋放資源
        await context.close()
        await browser.close()

    # 計算執行總耗時
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "=" * 80)
    print(f"✓ 所有品類跨賣場抓取完成！總耗時僅：{elapsed:.2f} 秒 (非同步併發加速)")
    print("=" * 80)

    # ==========================================================================
    # 4. 終端機報表輸出 (Console Output)
    # ⚠️ 商業倫理說明：各商品包裝規格（如 1000g vs 300gX12盒）不同，
    #    僅列出客觀售價，不直接進行相減計算優劣。
    # ==========================================================================
    print("\n📊 【毛寶 vs 競品 多賣場即時價格監控報表】")
    print("註：因各商品包裝規格與單位不同，本報表僅呈現原始監控售價，不進行價差比較與優勢計算")
    print("-" * 90)
    print(f"{'品類':<12} {'品牌':<8} {'賣場':<12} {'搜尋商品標題':<32} {'售價'}")
    print("-" * 90)

    for cat_data in all_results:
        cat_name = cat_data["category"]
        all_prods = [cat_data["maobao_product"]] + cat_data["competitors"]

        for prod_idx, prod in enumerate(all_prods):
            brand_label = f"[{prod['brand']}]"
            is_first_store = True

            for store in prod["stores"]:
                title_short = (store["title"][:30] + "..") if len(store["title"]) > 30 else store["title"]
                price_str = f"${store['price']}" if store["price"] > 0 else "未找到"
                
                cat_disp = cat_name if (prod_idx == 0 and is_first_store) else ""
                brand_disp = brand_label if is_first_store else ""

                print(f"{cat_disp:<12} {brand_disp:<8} {store['platform']:<12} {title_short:<32} {price_str}")
                is_first_store = False
        print("-" * 90)

    # ==========================================================================
    # 5. 匯出 JSON 詳細數據 (JSON Export for System Integration)
    # ==========================================================================
    report_json_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": round(elapsed, 2),
        "platforms": platform_names,
        "note": "單位與包裝規格不同，無輸出價差比較與優劣分析",
        "data": all_results
    }
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report_json_data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 已匯出 JSON 詳細數據：{REPORT_JSON}")

    # ==========================================================================
    # 6. 匯出 GFM Markdown 分析報告 (GFM Markdown Export for PM Reporting)
    # ==========================================================================
    md_content = f"# 毛寶企業 產品與競品多賣場價格監控日報\n\n"
    md_content += f"- **監控時間**：{report_json_data['timestamp']}\n"
    md_content += f"- **總耗時**：{elapsed:.2f} 秒 (Playwright Async 多賣場平行併發)\n"
    md_content += f"- **監控賣場**：{', '.join(platform_names)}\n"
    md_content += f"- **說明**：*因各品牌商品與包裝規格單位不一，本報告僅呈現各平台即時監控價格與標題，不進行價差比較。*\n\n"
    md_content += f"## 📊 跨賣場價格一覽表\n\n"
    md_content += f"| 品類 | 品牌 | 賣場平台 | 搜尋商品標題 | 售價 (TWD) | 商品連結 |\n"
    md_content += f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for cat_data in all_results:
        cat_name = cat_data["category"]
        all_prods = [cat_data["maobao_product"]] + cat_data["competitors"]

        for prod in all_prods:
            brand_label = f"**{prod['brand']}**" if prod['brand'] == '毛寶' else prod['brand']
            for store in prod["stores"]:
                price_disp = f"**${store['price']}**" if store["price"] > 0 else "N/A"
                url_disp = f"[商品連結]({store['url']})" if store['url'] else "N/A"
                md_content += f"| {cat_name} | {brand_label} | {store['platform']} | {store['title']} | {price_disp} | {url_disp} |\n"

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✓ 已匯出 Markdown 分析報告：{REPORT_MD}")


if __name__ == "__main__":
    # 使用 asyncio.run() 啟動 Python Event Loop
    asyncio.run(main())
