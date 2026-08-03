"""
stock_batch_scraper.py
----------------------------------------
Playwright 非同步股票批次爬蟲模組。
包含：
1. 單一股票抓取 (Async)
2. 併發與速率控制 (asyncio.Semaphore) 批次爬取
3. 批次結果匯出 (CSV / JSON)
"""

import os
import csv
import json
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright, BrowserContext

async def fetch_single_stock(context: BrowserContext, stock_code: str) -> Dict:
    """
    使用給定的 BrowserContext 爬取單一股票即時資訊
    """
    clean_code = stock_code.strip()
    target_code = f"{clean_code}.TW" if not (clean_code.endswith(".TW") or clean_code.endswith(".TWO")) else clean_code
    url = f"https://tw.stock.yahoo.com/quote/{target_code}"
    
    page = await context.new_page()
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
        
        # 3. 漲跌資訊
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
        await page.close()

async def batch_fetch_stocks(stock_codes: List[str], max_concurrency: int = 3) -> List[Dict]:
    """
    使用 Playwright 非同步併發抓取多支股票資料，並使用 Semaphore 進行流量與併行數限制
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
                print(f"⏳ [併行抓取中] 股票代碼: {code} ...")
                data = await fetch_single_stock(context, code)
                # 微小的請求間隔保護伺服器
                await asyncio.sleep(0.5)
                return data
                
        tasks = [worker(code) for code in stock_codes]
        results = await asyncio.gather(*tasks)
        await browser.close()
        
    return results

def export_to_csv(data_list: List[Dict], filepath: str = "output/stocks_batch.csv"):
    """將批次股票資料匯出為 CSV 檔案"""
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
