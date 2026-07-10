from playwright.sync_api import sync_playwright

# 使用 Playwright 啟動瀏覽器並執行自動化腳本
with sync_playwright() as p:
    # 啟動 Chromium 瀏覽器（無界面模式）
    browser = p.chromium.launch(headless=True)
    # 開啟一個新的頁面
    page = browser.new_page()
    # 前往 PTT 爆爆板首頁
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")

    # 等待確認年齡的按鈕出現（最多等待 10 秒）
    page.wait_for_selector("button.btn-big", timeout=10000)
    # 點擊「我同意，我已年滿十八歲」按鈕
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()

    # 等待內容區塊載入完成（最多等待 10 秒）
    page.wait_for_selector("div.r-ent", timeout=10000)
    # 取得目前頁面的標題並印出
    title = page.title()
    print(f"頁面標題: {title}")

    # 選取所有文章標題連結並存入列表
    articles = page.locator("div.r-ent div.title a").all()
    print(f"文章數量: {len(articles)}")
    # 印出前 5 篇文章的標題文字
    for article in articles[:5]:
        print(f"  - {article.inner_text()}")

    # 將整個頁面截圖並儲存至檔案
    page.screenshot(path="ptt_screenshot.png", full_page=True)
    print("截圖已儲存: ptt_screenshot.png")

    # 關閉瀏覽器
    browser.close()
