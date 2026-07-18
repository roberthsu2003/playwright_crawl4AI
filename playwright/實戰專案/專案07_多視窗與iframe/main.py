"""專案 07：一次練習 popup、JavaScript alert 與 iframe。"""

from playwright.sync_api import sync_playwright


BASE_URL = "https://the-internet.herokuapp.com"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto(f"{BASE_URL}/windows")
    with page.expect_popup() as popup_info:
        page.get_by_role("link", name="Click Here").click()
    popup = popup_info.value
    popup.wait_for_load_state()
    print(f"新分頁: {popup.get_by_role('heading').inner_text()}")
    popup.close()

    page.goto(f"{BASE_URL}/javascript_alerts")
    page.once("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Click for JS Alert").click()
    print(f"Alert 結果: {page.locator('#result').inner_text()}")

    page.goto(f"{BASE_URL}/iframe")
    editor = page.frame_locator("#mce_0_ifr").locator("body#tinymce")
    editor.wait_for(state="visible")
    print(f"iframe 內容: {editor.inner_text()}")

    context.close()
    browser.close()
