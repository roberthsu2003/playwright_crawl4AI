from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)
    title = page.title()
    print(f"頁面標題: {title}")

    articles = page.locator("div.r-ent div.title a").all()
    print(f"文章數量: {len(articles)}")
    for article in articles[:5]:
        print(f"  - {article.inner_text()}")

    page.screenshot(path="ptt_screenshot.png", full_page=True)
    print("截圖已儲存: ptt_screenshot.png")
    browser.close()
    
