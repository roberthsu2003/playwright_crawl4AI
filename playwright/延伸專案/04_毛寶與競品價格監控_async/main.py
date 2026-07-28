import asyncio
import json
import os
import re
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any
from playwright.async_api import async_playwright, BrowserContext, Page

CONFIG_FILE = "products_config.json"
REPORT_JSON = "price_report.json"
REPORT_MD = "price_report.md"


async def fetch_pchome(context: BrowserContext, keyword: str) -> Dict[str, Any]:
    """從 PChome 24h 購物抓取第一筆商品資訊"""
    result = {
        "platform": "PChome 24h",
        "title": "未找到相關商品",
        "price": 0,
        "url": "",
        "status": "無結果"
    }

    encoded_kw = urllib.parse.quote(keyword)
    api_url = f"https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={encoded_kw}&page=1"

    try:
        response = await context.request.get(api_url, timeout=10000)
        if response.status == 200:
            data = await response.json()
            prods = data.get("prods", [])
            if prods:
                item = prods[0]
                result["title"] = item.get("name", "未知的商品標題")
                result["price"] = int(item.get("price", 0))
                result["url"] = f"https://24h.pchome.com.tw/prod/{item.get('Id', '')}"
                result["status"] = "成功"
                return result
    except Exception:
        pass

    return result


async def fetch_momo(context: BrowserContext, keyword: str) -> Dict[str, Any]:
    """從 momo購物網 抓取第一筆商品資訊"""
    result = {
        "platform": "momo購物網",
        "title": "未找到相關商品",
        "price": 0,
        "url": "",
        "status": "無結果"
    }

    encoded_kw = urllib.parse.quote(keyword)
    url = f"https://www.momoshop.com.tw/search/searchShop.jsp?keyword={encoded_kw}"
    page: Page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(1000)
        cards = page.locator("div.listArea ul li, .prdListArea ul li")
        
        if await cards.count() > 0:
            card = cards.first
            title_loc = card.locator(".prdName, h3, .goodsName")
            price_loc = card.locator(".price, .money, .prdPrice")
            link_loc = card.locator("a.goods-img-url, a.prdName, a").first

            title = await title_loc.first.inner_text() if await title_loc.count() > 0 else ""
            price_text = await price_loc.first.inner_text() if await price_loc.count() > 0 else ""
            href = await link_loc.get_attribute("href") if await link_loc.count() > 0 else ""

            digits = re.sub(r"[^\d]", "", price_text)
            price = int(digits) if digits else 0

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
        await page.close()

    return result


async def fetch_yahoo(context: BrowserContext, keyword: str) -> Dict[str, Any]:
    """從 Yahoo購物中心 抓取第一筆商品資訊"""
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


async def fetch_item_across_platforms(context: BrowserContext, brand: str, name: str, keyword: str) -> Dict[str, Any]:
    """在各大賣場 (PChome, momo, Yahoo) 平行併發查詢該商品資訊"""
    stores_tasks = [
        fetch_pchome(context, keyword),
        fetch_momo(context, keyword),
        fetch_yahoo(context, keyword)
    ]
    store_results = await asyncio.gather(*stores_tasks)

    return {
        "brand": brand,
        "name": name,
        "keyword": keyword,
        "stores": store_results
    }


async def monitor_category_async(context: BrowserContext, category_item: Dict[str, Any]) -> Dict[str, Any]:
    """非同步處理單一品類（包含毛寶與競品，平行抓取各大賣場）"""
    category_name = category_item["category"]
    maobao_cfg = category_item["maobao_product"]
    competitors_cfg = category_item["competitors"]

    print(f"🚀 開始平行併發查詢品類：【{category_name}】跨賣場數據...")

    tasks = [
        fetch_item_across_platforms(context, "毛寶", maobao_cfg["name"], maobao_cfg["keyword"])
    ]
    for comp in competitors_cfg:
        tasks.append(fetch_item_across_platforms(context, comp["brand"], comp["name"], comp["keyword"]))

    results = await asyncio.gather(*tasks)

    return {
        "category": category_name,
        "maobao_product": results[0],
        "competitors": results[1:]
    }


async def main():
    print("=" * 80)
    print("毛寶企業 (Maobao) 多賣場產品與競品價格每日監控系統 [Playwright Async版]")
    print("=" * 80)

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

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context: BrowserContext = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )

        cat_tasks = [monitor_category_async(context, cat) for cat in categories]
        all_results = await asyncio.gather(*cat_tasks)

        await context.close()
        await browser.close()

    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "=" * 80)
    print(f"✓ 所有品類跨賣場抓取完成！總耗時僅：{elapsed:.2f} 秒 (非同步併發加速)")
    print("=" * 80)

    # 輸出終端機各賣場價格資訊 (注意：單位不同，不進行價差比較與優劣分析)
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

    # 匯出 JSON 詳細數據
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

    # 匯出 Markdown 報表
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
    asyncio.run(main())
