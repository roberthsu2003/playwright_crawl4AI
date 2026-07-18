from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://zh.wikipedia.org")
    page.fill("input#searchInput", "Python")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    print(f"[networkidle] 標題: {page.title()}")

    page.goto("https://zh.wikipedia.org")
    page.fill("input#searchInput", "Playwright")
    page.keyboard.press("Enter")
    page.wait_for_selector("#firstHeading", timeout=10000)
    heading = page.locator("#firstHeading").inner_text()
    print(f"[wait_for_selector] 找到: {heading}")

    page.goto("https://zh.wikipedia.org")
    page.fill("input#searchInput", "自動化測試")
    with page.expect_navigation():
        page.keyboard.press("Enter")
    print(f"[expect_navigation] 標題: {page.title()}")

    browser.close()
