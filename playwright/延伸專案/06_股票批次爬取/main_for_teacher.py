"""
================================================================================
專案 06：股票批次爬取 (Async Playwright 版) [教師上課教學講義版]
--------------------------------------------------------------------------------
檔案名稱：main_for_teacher.py
教學目標：
1. 掌握 Async Playwright (async_api) 搭配 `asyncio` 的非同步併發架構
2. 學習 `asyncio.Semaphore` 流量控制 (Rate Limiting) 與最大並行數保護
3. 整合第三方套件 (`twstock`) 實現命令列 (CLI) 關鍵字搜尋與選取邏輯
4. 學習批次數據結構處理與轉存 (CSV / JSON)
5. 了解無 GUI 架構設計：將數據邏輯解耦，方便未來使用 Vibe Coding 工具產生 UI
================================================================================
"""

import os
import sys
import csv
import json
import time
import asyncio
from typing import List, Dict
import twstock
from playwright.async_api import async_playwright, BrowserContext, Page

# ==============================================================================
# 1. 爬蟲核心模組：單一股票與併發批次爬取 (Scraping Core)
# ==============================================================================

async def fetch_single_stock(context: BrowserContext, stock_code: str) -> Dict:
    """
    【單一股票抓取函式】
    💡 教師說明：
       利用傳入的 `BrowserContext` 建立獨立 `Page` 進行抓取。
       在 Playwright 中，多個 `Page` 可以共用同一個 `BrowserContext`，
       這樣不需要重複開關實體瀏覽器進程 (Browser)，開銷極低且速度極快！
    """
    clean_code = stock_code.strip()
    target_code = f"{clean_code}.TW" if not (clean_code.endswith(".TW") or clean_code.endswith(".TWO")) else clean_code
    url = f"https://tw.stock.yahoo.com/quote/{target_code}"
    
    page: Page = await context.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_selector("h1", timeout=10000)
        
        # 1. 股票名稱
        h1_texts = await page.locator("h1").all_inner_texts()
        stock_name = "未知股票"
        for t in h1_texts:
            if t.strip() and t.strip() != "Yahoo股市":
                stock_name = t.strip()
                break

        # 2. 即時價格
        price_el = page.locator("span[class*='Fz(32px)']").first
        price = await price_el.inner_text() if await price_el.count() > 0 else "N/A"
        
        # 3. 漲跌金額與幅度
        chg_el = page.locator("span[class*='Fz(20px)']").first
        chg_info = await chg_el.inner_text() if await chg_el.count() > 0 else "0.00"
        chg_info = chg_info.replace("\n", " ").strip()
        
        # 4. 資料時間
        time_el = page.locator("span:has-text('資料時間')").first
        time_str = await time_el.inner_text() if await time_el.count() > 0 else ""
        time_clean = time_str.replace("資料時間：", "").strip()
        
        # 5. 詳細數據
        details = {}
        list_items = page.locator("ul[class*='D(f)'] li")
        item_count = await list_items.count()
        for i in range(item_count):
            raw_text = await list_items.nth(i).inner_text()
            lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
            if len(lines) >= 2:
                details[lines[0]] = lines[1]

        return {
            "股票代碼": clean_code,
            "股票名稱": stock_name,
            "即時價格": price,
            "漲跌資訊": chg_info,
            "資料時間": time_clean,
            "開盤價": details.get("開盤", "N/A"),
            "最高價": details.get("最高", "N/A"),
            "最低價": details.get("最低", "N/A"),
            "昨收價": details.get("昨收", "N/A")
        }
    except Exception as e:
        return {
            "股票代碼": clean_code,
            "股票名稱": "抓取失敗",
            "即時價格": "N/A",
            "錯誤訊息": str(e)
        }
    finally:
        # 完成後關閉頁面，釋放記憶體
        await page.close()


async def batch_fetch_stocks(stock_codes: List[str], max_concurrency: int = 3) -> List[Dict]:
    """
    【批次併發抓取函式 (Semaphore 流量與併行控制)】
    💡 教師說明：
       1. 若直接對 20 支股票發起併行，可能會瞬間擠爆網路或被目標網站封鎖 IP。
       2. 使用 `asyncio.Semaphore(max_concurrency)` 建立信號量閥門，控制最多同時只有
          `max_concurrency` (例如 3 個) 任務在執行。
       3. 搭配 `asyncio.gather(*tasks)`，當一個分頁完成時，下一個股票任務會自動補上。
    """
    semaphore = asyncio.Semaphore(max_concurrency)
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        
        async def worker(code: str):
            async with semaphore:
                print(f"⏳ [Semaphore 限流控制] 正在併行抓取股票: {code} ...")
                data = await fetch_single_stock(context, code)
                # 微小間隔時間，對目標伺服器展現友善爬蟲行為
                await asyncio.sleep(0.5)
                return data
                
        tasks = [worker(code) for code in stock_codes]
        results = await asyncio.gather(*tasks)
        await browser.close()
        
    return results


# ==============================================================================
# 2. 資料匯出模組 (Data Export Functions)
# ==============================================================================

def export_to_csv(data_list: List[Dict], filepath: str = "output/stocks_batch.csv"):
    """將批次股票資料匯出為 CSV 檔案 (使用 utf-8-sig 解決 Excel 開啟中文亂碼問題)"""
    if not data_list:
        return
        
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = list(data_list[0].keys())
    
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)
        
    print(f"✅ 資料已成功匯出至 CSV 檔案: {filepath}")

def export_to_json(data_list: List[Dict], filepath: str = "output/stocks_batch.json"):
    """將批次股票資料匯出為 JSON 檔案"""
    if not data_list:
        return
        
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)
        
    print(f"✅ 資料已成功匯出至 JSON 檔案: {filepath}")


# ==============================================================================
# 3. 搜尋與 CLI 互動模組 (Search & CLI Menu)
# ==============================================================================

def search_stocks_with_twstock(query: str) -> list[dict]:
    """使用 twstock 根據代碼或名稱關鍵字過濾股票"""
    query = query.strip().lower()
    results = []
    
    for code, info in twstock.codes.items():
        if len(code) == 4 and (info.type == '股票' or getattr(info, 'market', '') in ['上市', '上櫃']):
            if query in code.lower() or query in info.name.lower():
                results.append({
                    "code": code,
                    "name": info.name,
                    "market": getattr(info, 'market', '台股'),
                    "group": getattr(info, 'group', '')
                })
    return results

def display_batch_results(data_list: list[dict]):
    """在終端機印出美化對齊的批次表格"""
    print("\n" + "=" * 90)
    print(f"{'股票代碼':<10} {'股票名稱':<12} {'即時價格':<12} {'漲跌金額/幅度':<16} {'資料更新時間':<20}")
    print("-" * 90)
    
    for item in data_list:
        code = item.get("股票代碼", "N/A")
        name = item.get("股票名稱", "N/A")
        price = item.get("即時價格", "N/A")
        chg = item.get("漲跌資訊", "N/A")
        time_str = item.get("資料時間", "N/A")
        
        print(f"{code:<10} {name:<12} {price:<12} {chg:<16} {time_str:<20}")
        
    print("=" * 90 + "\n")

async def run_batch_scrape(stock_codes: list[str]):
    """執行批次抓取並計算總耗時"""
    print(f"\n🚀 開始批次爬取 {len(stock_codes)} 支股票: {', '.join(stock_codes)}")
    start_time = time.time()
    
    # 呼叫 async 併發抓取核心
    results = await batch_fetch_stocks(stock_codes, max_concurrency=3)
    elapsed = time.time() - start_time
    
    print(f"\n✨ 批次爬取完成！總耗時僅: {elapsed:.2f} 秒 (Semaphore 平行併發加速)")
    display_batch_results(results)
    
    return results

def cli_menu():
    """命令列 (CLI) 文字選單介面"""
    default_popular_stocks = ["2330", "2317", "2454", "2308", "3008"]
    last_results = []
    
    while True:
        print("\n==========================================")
        print(" 📈 Playwright 股票批次爬取系統 [教學備課版]")
        print("==========================================")
        print(" [1] 預設熱門股票批次抓取 (2330, 2317, 2454, 2308, 3008)")
        print(" [2] 關鍵字搜尋股票並選擇批次抓取 (twstock)")
        print(" [3] 自訂股票代碼清單 (逗號分隔)")
        print(" [4] 匯出最近一次抓取結果 (CSV / JSON)")
        print(" [0] 離開系統")
        print("------------------------------------------")
        
        choice = input("請選擇操作選項 (0-4): ").strip()
        
        if choice == "1":
            last_results = asyncio.run(run_batch_scrape(default_popular_stocks))
            
        elif choice == "2":
            keyword = input("\n請輸入股票代碼或名稱關鍵字 (例如 23 或 晶圓): ").strip()
            if not keyword:
                print("⚠️ 關鍵字不可為空！")
                continue
                
            matches = search_stocks_with_twstock(keyword)
            if not matches:
                print(f"❌ 查無符合 '{keyword}' 的股票！")
                continue
                
            print(f"\n找到 {len(matches[:20])} 筆符合條件的股票 (最多顯示 20 筆):")
            for idx, item in enumerate(matches[:20], 1):
                print(f" [{idx:2d}] {item['code']} - {item['name']} ({item['market']})")
                
            input_indices = input("\n請輸入要爬取的序號 (例如 1,2,3 或 'all'): ").strip()
            if not input_indices:
                continue
                
            selected_codes = []
            if input_indices.lower() == "all":
                selected_codes = [item['code'] for item in matches[:20]]
            else:
                for parts in input_indices.split(","):
                    if parts.strip().isdigit():
                        idx = int(parts.strip()) - 1
                        if 0 <= idx < len(matches[:20]):
                            selected_codes.append(matches[idx]['code'])
                            
            if selected_codes:
                last_results = asyncio.run(run_batch_scrape(selected_codes))
            else:
                print("⚠️ 未選擇任何有效股票！")
                
        elif choice == "3":
            user_input = input("\n請輸入股票代碼清單 (用逗號分隔，例: 2330, 2317): ").strip()
            if not user_input:
                print("⚠️ 代碼不可為空！")
                continue
            codes = [c.strip() for c in user_input.split(",") if c.strip()]
            if codes:
                last_results = asyncio.run(run_batch_scrape(codes))
                
        elif choice == "4":
            if not last_results:
                print("⚠️ 目前無抓取結果可供匯出，請先執行爬取作業！")
                continue
            export_choice = input("請選擇匯出格式 (1: CSV, 2: JSON, 3: 兩者皆是): ").strip()
            if export_choice in ["1", "3"]:
                export_to_csv(last_results)
            if export_choice in ["2", "3"]:
                export_to_json(last_results)
                
        elif choice == "0":
            print("\n👋 感謝使用股票批次爬取系統！")
            break
        else:
            print("⚠️ 無效選項，請重新輸入！")

async def main():
    # 支援直接傳參非互動批次爬取，例: uv run python main_for_teacher.py 2330 2317 2454
    if len(sys.argv) > 1:
        stock_codes = sys.argv[1:]
        results = await run_batch_scrape(stock_codes)
        export_to_csv(results)
    else:
        cli_menu()

if __name__ == "__main__":
    asyncio.run(main())
