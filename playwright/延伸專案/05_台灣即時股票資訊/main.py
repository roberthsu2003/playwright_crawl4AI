"""
05_台灣即時股票資訊 (Playwright 版)
----------------------------------------
本專案示範如何使用 Playwright 擷取台灣即時股票資訊（以台積電 2330 為預設目標）。
練習重點：
1. Playwright 瀏覽器初始化與 Context 設定
2. 動態 DOM 載入與 Locator 定位
3. 即時行情數據擷取與結構化處理
4. 終端機格式化報表輸出 (無 GUI)
"""

import sys
import asyncio
from playwright.async_api import async_playwright

async def fetch_stock_quote(stock_code: str = "2330") -> dict:
    """
    使用 Playwright 爬取指定股票代碼之即時行情數據
    
    :param stock_code: 股票代碼 (例: "2330", "2317")
    :return: 包含股票即時數據的字典
    """
    clean_code = stock_code.strip()
    # 支援台股格式: TWSE 使用 .TW
    target_code = f"{clean_code}.TW" if not (clean_code.endswith(".TW") or clean_code.endswith(".TWO")) else clean_code
    url = f"https://tw.stock.yahoo.com/quote/{target_code}"
    
    async with async_playwright() as p:
        # 啟動 Chromium 瀏覽器
        browser = await p.chromium.launch(headless=True)
        
        # 建立獨立 BrowserContext，配置 User-Agent 模擬真實瀏覽器行為
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        
        try:
            print(f"🚀 前往目標頁面: {url} ...")
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            
            # 等待核心元素載入
            await page.wait_for_selector("h1", timeout=10000)
            
            # 1. 擷取股票名稱與代碼
            h1_texts = await page.locator("h1").all_inner_texts()
            # 排除非目標標題
            stock_name = "未知股票"
            for t in h1_texts:
                if t.strip() and t.strip() != "Yahoo股市":
                    stock_name = t.strip()
                    break
            
            # 2. 擷取成交即時價格
            price_el = page.locator("span[class*='Fz(32px)']").first
            price = await price_el.inner_text() if await price_el.count() > 0 else "N/A"
            
            # 3. 擷取漲跌資訊與幅度
            chg_el = page.locator("span[class*='Fz(20px)']").first
            chg_info = await chg_el.inner_text() if await chg_el.count() > 0 else "0.00"
            chg_info = chg_info.replace("\n", " ").strip()
            
            # 4. 擷取資料更新時間
            time_el = page.locator("span:has-text('資料時間')").first
            time_str = await time_el.inner_text() if await time_el.count() > 0 else ""
            time_clean = time_str.replace("資料時間：", "").strip()
            
            # 5. 擷取詳細行情資訊區塊 (開盤、昨收、最高、最低、成交量)
            details = {}
            list_items = page.locator("ul[class*='D(f)'] li")
            item_count = await list_items.count()
            
            for i in range(item_count):
                raw_text = await list_items.nth(i).inner_text()
                lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
                if len(lines) >= 2:
                    label = lines[0]
                    value = lines[1]
                    details[label] = value

            return {
                "股票代碼": clean_code,
                "股票名稱": stock_name,
                "即時價格": price,
                "漲跌金額/幅度": chg_info,
                "資料時間": time_clean,
                "開盤價": details.get("開盤", "N/A"),
                "最高價": details.get("最高", "N/A"),
                "最低價": details.get("最低", "N/A"),
                "昨收價": details.get("昨收", "N/A"),
                "成交量": details.get("成交量", "N/A")
            }
            
        except Exception as e:
            print(f"❌ 擷取股票 [{clean_code}] 發生錯誤: {e}")
            return {
                "股票代碼": clean_code,
                "股票名稱": "擷取失敗",
                "錯誤訊息": str(e)
            }
        finally:
            await browser.close()

def display_stock_info(data: dict):
    """在終端機中格式化印出即時股票資訊報表"""
    print("\n" + "=" * 60)
    print(f"📊 台灣即時股票資訊報表 - [{data.get('股票名稱', 'N/A')}] ({data.get('股票代碼', '')})")
    print("=" * 60)
    
    if "錯誤訊息" in data:
        print(f"⚠️  錯誤: {data['錯誤訊息']}")
        print("=" * 60 + "\n")
        return

    print(f"📈 即時成交價 : {data.get('即時價格', 'N/A')}")
    print(f"💹 漲跌金額/幅: {data.get('漲跌金額/幅度', 'N/A')}")
    print(f"🕒 資料更新時間: {data.get('資料時間', 'N/A')}")
    print("-" * 60)
    print(f"🔓 開盤價 : {data.get('開盤價', 'N/A'):<15} 🔒 昨收價 : {data.get('昨收價', 'N/A')}")
    print(f"🔺 最高價 : {data.get('最高價', 'N/A'):<15} 🔻 最低價 : {data.get('最低價', 'N/A')}")
    print(f"📊 成交量 : {data.get('成交量', 'N/A')}")
    print("=" * 60)
    print("💡 提示：本數據僅供教學示範與即時顯示，核心程式不預設儲存歷史庫。\n")

async def main():
    # 支援命令行傳參，例: uv run main.py 2317
    stock_code = sys.argv[1] if len(sys.argv) > 1 else "2330"
    print(f"🔍 準備查詢股票代碼: {stock_code}")
    
    stock_data = await fetch_stock_quote(stock_code)
    display_stock_info(stock_data)

if __name__ == "__main__":
    asyncio.run(main())
