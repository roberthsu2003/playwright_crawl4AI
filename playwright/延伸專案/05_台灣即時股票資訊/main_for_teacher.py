"""
================================================================================
專案 05：台灣即時股票資訊爬蟲 [教師上課教學講義版]
--------------------------------------------------------------------------------
檔案名稱：main_for_teacher.py
教學目標：
1. 掌握 Playwright 非同步 API (async_api) 啟動與基礎配置概念
2. 理解 Browser、BrowserContext 與 Page 的三層架構與資源管理
3. 學習網頁動態 DOM 元素定位器 (Locators) 與選擇器寫法
4. 掌握網頁載入等待策略：`wait_until="domcontentloaded"` 與 `wait_for_selector`
5. 理解即時資料快照架構與「無 GUI 依賴、未來靠 Vibe Coding 產生 UI」的設計理念
================================================================================
"""

import sys
import asyncio
from playwright.async_api import async_playwright

# ==============================================================================
# 1. 核心爬蟲函式 (Core Scraping Function)
# ==============================================================================

async def fetch_stock_quote(stock_code: str = "2330") -> dict:
    """
    使用 Playwright 非同步 API 爬取指定台股代碼之即時行情
    
    💡 教師說明重點：
    1. 【URL 格式處理】：台灣上市股票在國際平台 (如 Yahoo 股市) 預設需帶有 `.TW` 後綴 (如 2330.TW)。
    2. 【BrowserContext】：建立獨立隱私會話，設定 User-Agent 避免遭目標網站辨識為無標頭爬蟲 (Bot)。
    3. 【非同步生命週期】：使用 `async with` 確保程式發生例外時瀏覽器進程也會被正確關閉。
    
    :param stock_code: 股票代碼 (例如 "2330", "2317")
    :return: 包含行情資料的字典 (dict)
    """
    clean_code = stock_code.strip()
    target_code = f"{clean_code}.TW" if not (clean_code.endswith(".TW") or clean_code.endswith(".TWO")) else clean_code
    url = f"https://tw.stock.yahoo.com/quote/{target_code}"
    
    async with async_playwright() as p:
        # 步驟 A: 啟動 Chromium 瀏覽器進程
        # (教學示範時可設定 headless=False 讓學生看見瀏覽器打開畫面的過程)
        browser = await p.chromium.launch(headless=True)
        
        # 步驟 B: 建立隱私上下文 (Context) 並注入模擬真實使用者的 User-Agent
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        
        try:
            print(f"🚀 [1/3] 正在前往目標行情頁面: {url} ...")
            # 💡 等待策略：使用 domcontentloaded 迅速通過，避免等待輪播廣告或 websocket
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            
            print(f"⏳ [2/3] 等待動態 DOM 核心標題元素載入...")
            # 💡 元素等待：等待 <h1> 標題元素渲染完畢再進行提取
            await page.wait_for_selector("h1", timeout=10000)
            
            print(f"🔍 [3/3] 正在解析與提取各欄位數據...")
            
            # --- 欄位 1: 股票名稱與代碼 ---
            # 💡 Playwright 嚴格模式 (Strict Mode) 提醒：
            #    當頁面有多個 <h1> 時，`page.locator('h1').inner_text()` 會觸發 strict mode 錯誤。
            #    使用 `all_inner_texts()` 抓取所有 <h1> 內容再過濾，是最安全穩健的寫法。
            h1_texts = await page.locator("h1").all_inner_texts()
            stock_name = "未知股票"
            for t in h1_texts:
                if t.strip() and t.strip() != "Yahoo股市":
                    stock_name = t.strip()
                    break
            
            # --- 欄位 2: 即時成交價 ---
            # 使用包含 class 名稱模糊匹配 `span[class*='Fz(32px)']` 取出第一筆文字
            price_el = page.locator("span[class*='Fz(32px)']").first
            price = await price_el.inner_text() if await price_el.count() > 0 else "N/A"
            
            # --- 欄位 3: 漲跌金額與幅度 ---
            chg_el = page.locator("span[class*='Fz(20px)']").first
            chg_info = await chg_el.inner_text() if await chg_el.count() > 0 else "0.00"
            chg_info = chg_info.replace("\n", " ").strip()
            
            # --- 欄位 4: 資料更新時間 ---
            # 使用文字包含定位器 `span:has-text('資料時間')`
            time_el = page.locator("span:has-text('資料時間')").first
            time_str = await time_el.inner_text() if await time_el.count() > 0 else ""
            time_clean = time_str.replace("資料時間：", "").strip()
            
            # --- 欄位 5: 詳細行情明細 (開盤、昨收、最高、最低、成交量) ---
            # 利用選單列表迴圈對應 label 與 value
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
            print(f"❌ 擷取股票 [{clean_code}] 發生例外錯誤: {e}")
            return {
                "股票代碼": clean_code,
                "股票名稱": "擷取失敗",
                "錯誤訊息": str(e)
            }
        finally:
            # 關閉瀏覽器釋放系統資源
            await browser.close()


# ==============================================================================
# 2. 終端機格式化報表輸出 (Console Display Function)
# ==============================================================================

def display_stock_info(data: dict):
    """
    在終端機中格式化印出即時股票資訊報表
    
    💡 設計理念與架構說明：
    1. 本專案完全「去 GUI 依賴」，專注於核心資料抓取與轉換。
    2. 學生學會核心 API 後，未來可透過 Vibe Coding (AI 賦能) 輕鬆為此資料結構套上 GUI 介面。
    3. 本專案預設不寫入資料庫，強調「即時快照 Display」理念。
    """
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
    print("💡 教學提示：核心程式不預設儲存歷史庫，資料僅用於即時顯示。\n")


# ==============================================================================
# 3. 主程式進入點 (Main Entry)
# ==============================================================================

async def main():
    # 支援命令列傳入股票代碼，例: uv run python main_for_teacher.py 2317
    stock_code = sys.argv[1] if len(sys.argv) > 1 else "2330"
    print(f"🔍 [教學示範] 準備查詢股票代碼: {stock_code}")
    
    stock_data = await fetch_stock_quote(stock_code)
    display_stock_info(stock_data)

if __name__ == "__main__":
    asyncio.run(main())
