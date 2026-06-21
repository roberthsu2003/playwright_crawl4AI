from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://zh.wikipedia.org")

    print("=== 鍵盤操作 ===")
    page.fill("input#searchInput", "滑鼠")
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    print(f"搜尋結果: {page.title()}")

    page.goto("https://zh.wikipedia.org")
    page.wait_for_load_state("networkidle")

    print("\n=== 滾動操作 ===")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    print("已滾動至頁面底部再返回頂部")

    print("\n=== 懸停操作 ===")
    more_btn = page.get_by_role("button", name="阅读")
    if more_btn.count():
        more_btn.hover()
        page.wait_for_timeout(500)
        print("已懸停在「阅读」按鈕上")
    else:
        sidebar = page.locator("nav#p-navigation a").first
        if sidebar.count():
            sidebar.hover()
            print("已懸停在導航連結上")

    browser.close()
