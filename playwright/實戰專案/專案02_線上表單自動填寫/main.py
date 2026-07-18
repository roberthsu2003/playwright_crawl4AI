"""專案 02：自動完成 Selenium 官方測試表單。"""

from playwright.sync_api import sync_playwright


URL = "https://www.selenium.dev/selenium/web/web-form.html"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")

    page.get_by_label("Text input").fill("王小明")
    page.get_by_label("Password").fill("practice-only")
    page.get_by_label("Textarea").fill("這是 Playwright 表單自動化練習。")
    page.get_by_label("Dropdown (select)").select_option("2")

    checkbox = page.get_by_label("Default checkbox")
    if not checkbox.is_checked():
        checkbox.check()
    page.get_by_label("Default radio").check()

    page.get_by_role("button", name="Submit").click()
    page.wait_for_url("**/submitted-form.html**")
    message = page.get_by_text("Received!", exact=True)
    message.wait_for(state="visible")

    print(f"送出後網址: {page.url}")
    print(f"驗收訊息: {message.inner_text()}")
    browser.close()
