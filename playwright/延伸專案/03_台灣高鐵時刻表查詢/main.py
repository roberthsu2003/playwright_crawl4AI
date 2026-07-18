from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import json
import os

COOKIES_FILE = "thsrc_cookies.json"

with sync_playwright() as p:
    # 使用一般的 browser 和 context，只保存 cookies
    browser = p.chromium.launch(
        headless=False,
    )
    context = browser.new_context(viewport={"width": 1280, "height": 720})

    # 如果有保存的 cookies，載入它們
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r") as f:
            cookies = json.load(f)
            context.add_cookies(cookies)
        print("✓ 已載入保存的 cookies")

    page = context.new_page()
    page.goto("https://www.thsrc.com.tw/", wait_until="domcontentloaded")

    # 第一次訪問時，檢查並點擊"我同意"按鈕
    try:
        # 等待對話框出現（最多等待 3 秒）
        agree_button = page.locator('button:has-text("我同意")')
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
    page.locator("#select_location01").wait_for(state="visible", timeout=15000)
    print("✓ 頁面載入完成")

    # 選擇出發站：台北
    departure_station = page.locator("#select_location01")
    departure_station.select_option("台北")
    print("✓ 已選擇出發站：台北")

    # 選擇到達站：台中
    arrival_station = page.locator("#select_location02")
    arrival_station.select_option("台中")
    print("✓ 已選擇到達站：台中")

    # 計算當前時間加 1 小時
    now = datetime.now()
    departure_time = now + timedelta(hours=1)

    # 格式化日期和時間
    departure_date = departure_time.strftime("%Y/%m/%d")
    departure_hour = departure_time.strftime("%H:%M")

    print(f"\n✓ 自動設定出發時間為：{departure_date} {departure_hour}")

    # 填入出發日期
    date_input = page.locator("#Departdate01")
    date_input.click()  # 先點擊欄位
    date_input.fill("")  # 清空欄位
    date_input.fill(departure_date)  # 填入日期
    print(f"✓ 已填入出發日期：{departure_date}")

    # 填入出發時間
    time_input = page.locator("#outWardTime")
    time_input.click()  # 先點擊欄位
    time_input.fill("")  # 清空欄位
    time_input.fill(departure_hour)  # 填入時間
    print(f"✓ 已填入出發時間：{departure_hour}")

    # 等待一下確保輸入完成
    page.wait_for_timeout(1000)

    # 點擊查詢按鈕
    search_button = page.locator('button:has-text("查詢")')
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

    # 再等待一下確保所有資料都載入完成
    page.wait_for_timeout(2000)

    # 抓取時刻表資料
    print("=" * 60)
    print("時刻表資料")
    print("=" * 60)

    # 抓取所有車次資料（使用正確的選擇器）
    train_rows = page.locator("a.tr-row").all()

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

    # 等待票價表格出現
    try:
        page.locator('h2:has-text("車廂票價參考")').wait_for(state="visible", timeout=10000)
    except Exception:
        print("⚠ 票價資料可能尚未載入...")

    # 使用 JavaScript 抓取票價表格資料
    price_data = page.evaluate("""
        () => {
            const prices = [];
            const rows = document.querySelectorAll('table tr');
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td, th');
                if (cells.length > 0) {
                    const rowData = Array.from(cells).map(cell => cell.innerText.trim());
                    prices.push(rowData);
                }
            });
            
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
    page.wait_for_timeout(3000)

    browser.close()