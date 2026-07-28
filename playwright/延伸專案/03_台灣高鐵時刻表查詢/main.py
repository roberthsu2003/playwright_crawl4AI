from playwright.sync_api import sync_playwright
from playwright.sync_api import Playwright,Browser,BrowserContext,Page,Locator
from datetime import datetime, timedelta
import json
import os

COOKIES_FILE = "thsrc_cookies.json"

def crawl(p:Playwright):
    # 使用一般的 browser 和 context，只保存 cookies
    browser:Browser = p.chromium.launch(
        headless=False,
    )
    context:BrowserContext = browser.new_context(viewport={"width": 1280, "height": 720})

    # 如果有保存的 cookies，載入它們
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
            context.add_cookies(cookies)
        print("✓ 已載入保存的 cookies")

    page:Page = context.new_page()
    page.goto("https://www.thsrc.com.tw/", wait_until="domcontentloaded")

    # 第一次訪問時，檢查並點擊"我同意"按鈕
    try:
        # 等待對話框出現（最多等待 3 秒）
        agree_button = page.get_by_role("button", name="我同意")
        agree_button.click(timeout=3000)
        print("✓ 已點擊「我同意」按鈕")

        # 保存 cookies 到檔案
        cookies = context.cookies()
        with open(COOKIES_FILE, "w") as f:
            json.dump(cookies, f)
        print("✓ 已保存 cookies 到檔案")
    except Exception:
        print("✓ 沒有找到 cookies 對話框，可能已經同意過了")

    # 等待主要表單元素出現（表示頁面已經載入完成）
    print("正在等待頁面載入...")
    page.get_by_label("出發站").wait_for(state="visible", timeout=15000)
    print("✓ 頁面載入完成")

    # 選擇出發站：台北 (優先使用 Playwright 建議的 get_by_label)
    departure_station:Locator = page.get_by_label("出發站")
    departure_station.select_option("台北")
    print("✓ 已選擇出發站：台北")

    # 選擇到達站：台中 (優先使用 Playwright 建議的 get_by_label)
    arrival_station:Locator = page.get_by_label("到達站")
    arrival_station.select_option("台中")
    print("✓ 已選擇到達站：台中")

    # 計算當前時間加 1 小時
    now:datetime = datetime.now()
    departure_time:datetime = now + timedelta(hours=1)

    # 格式化日期和時間
    departure_date = departure_time.strftime("%Y/%m/%d")
    departure_hour = departure_time.strftime("%H:%M")

    print(f"\n✓ 自動設定出發時間為：{departure_date} {departure_hour}")

    # 填入出發日期 (優先使用 Playwright 建議的 get_by_label)
    date_input = page.get_by_label("出發日期")
    date_input.click()  # 先點擊欄位
    date_input.fill("")  # 清空欄位
    date_input.fill(departure_date)  # 填入日期
    print(f"✓ 已填入出發日期：{departure_date}")

    # 填入出發時間 (優先使用 Playwright 建議的 get_by_label)
    time_input = page.get_by_label("出發時間")
    time_input.click()  # 先點擊欄位
    time_input.fill("")  # 清空欄位
    time_input.fill(departure_hour)  # 填入時間
    print(f"✓ 已填入出發時間：{departure_hour}")

    # 按下 Tab 鍵讓欄位失焦並關閉選單
    page.keyboard.press("Tab")

    # 點擊查詢按鈕 (優先使用 Playwright 建議的 get_by_role)
    search_button = page.get_by_role("button", name="查詢").first
    search_button.click()
    print("✓ 已點擊查詢按鈕")

    # 等待查詢結果頁面載入
    page.wait_for_load_state("networkidle")
    print("正在等待查詢結果...")

    # 等待時刻表資料出現（最多等待 30 秒）
    try:
        page.locator("a.tr-row").first.wait_for(state="visible", timeout=30000)
        print("✓ 查詢結果已載入\n")
    except Exception:
        print("⚠ 等待超時，但繼續嘗試抓取資料...\n")

    # 抓取時刻表資料
    print("=" * 60)
    print("時刻表資料")
    print("=" * 60)

    # 抓取所有車次資料（使用 CSS Locator 處理集合資料）
    train_rows:list[Locator] = page.locator("a.tr-row").all()

    if train_rows:
        print(f"{'出發時間':<10} {'行車時間':<10} {'抵達時間':<10} {'車次':<8} {'自由座車廂'}")
        print("-" * 60)

        for row in train_rows:
            text = row.inner_text()
            # 移除多餘的空白和換行
            parts = text.replace("\n", " ").split()
            if len(parts) >= 5:
                departure = parts[0]
                duration = parts[1]
                arrival = parts[2]
                train_no = parts[3]
                free_seat = parts[4]
                print(f"{departure:<10} {duration:<10} {arrival:<10} {train_no:<8} {free_seat}")
    else:
        print("未找到車次資料")

    # 抓取票價資料
    print("\n" + "=" * 60)
    print("車廂票價參考")
    print("=" * 60)

    # 等待票價標題出現 (優先使用 Playwright 建議的 get_by_role / get_by_text)
    try:
        page.get_by_role("heading", name="車廂票價參考").wait_for(state="visible", timeout=10000)
    except Exception:
        print("⚠ 票價資料可能尚未載入...")

    # 使用 JavaScript 抓取票價表格資料 (在瀏覽器端執行，一次性傳回整張表格資料)
    price_data = page.evaluate("""
        () => {
            // 1. 建立一個空的 JavaScript 陣列，用來儲存最終整理好的票價表格資料
            const prices = [];
            
            // 2. 使用 document.querySelectorAll 找到網頁中所有表格的「資料列」(<tr> 標籤)
            const rows = document.querySelectorAll('table tr');
            
            // 3. 逐一遍歷每一列 (row)
            rows.forEach(row => {
                // 4. 取得當前這列裡面的所有「標頭欄位」(<th>) 與「一般欄位」(<td>)
                const cells = row.querySelectorAll('td, th');
                
                // 5. 確保這一列有欄位資料才進行處理
                if (cells.length > 0) {
                    // 6. Array.from(cells): 將抓到的欄位集合轉為標準 JS 陣列
                    //    .map(...): 迴圈處理每個欄位，讀取文字 (.innerText) 並清除前後空白 (.trim())
                    const rowData = Array.from(cells).map(cell => cell.innerText.trim());
                    
                    // 7. 將這一列整理好的資料 (rowData) 放入 prices 陣列中
                    prices.push(rowData);
                }
            });
            
            // 8. 回傳最終整理好的二維陣列 (格式如同 Python 的 list[list[str]])
            return prices;
        }
    """)

    if price_data:
        for row in price_data:
            print(" | ".join(row))
    else:
        print("未找到票價資料")

    # 抓取時刻表下載連結
    print("\n" + "=" * 60)
    print("時刻表下載")
    print("=" * 60)

    download_links = page.locator('a[description*="時刻表.pdf"]').all()
    for link in download_links:
        text = link.inner_text()
        url = link.get_attribute("href")
        print(f"• {text}")
        print(f"  連結: https://www.thsrc.com.tw{url}")

    print("\n" + "=" * 60)
    print("✓ 完成！")
    print("=" * 60)

    # 暫停一下讓你看到結果
    # 關閉 context 與 browser (關閉 context 會關閉其下所有頁面，關閉 browser 會釋放進程)
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        crawl(p)

    