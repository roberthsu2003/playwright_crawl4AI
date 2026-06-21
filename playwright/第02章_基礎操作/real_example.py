from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://zh.wikipedia.org")
    page.fill("input#searchInput", "臺灣")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    print(f"頁面標題: {page.title()}")

    first_heading = page.locator("#firstHeading").inner_text()
    print(f"搜尋主題: {first_heading}")

    content = page.locator("#mw-content-text p").first.inner_text()
    print(f"摘要: {content[:100]}...")

    page.go_back()
    page.wait_for_load_state("networkidle")
    print(f"返回首頁: {page.title()}")

    browser.close()
