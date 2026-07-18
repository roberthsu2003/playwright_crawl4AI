"""專案 04：正確等待延遲出現的動態內容。"""

from playwright.sync_api import expect, sync_playwright


URL = "https://the-internet.herokuapp.com/dynamic_loading/2"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_default_timeout(10_000)
    page.goto(URL, wait_until="domcontentloaded")

    # click() 會自動等待按鈕可操作。
    page.get_by_role("button", name="Start").click()

    # 明確等待元素可見。
    finish = page.locator("#finish h4")
    finish.wait_for(state="visible")

    # Web-first assertion 也會在 timeout 內自動重試。
    expect(finish).to_have_text("Hello World!")
    expect(page.locator("#loading")).to_be_hidden()

    print(f"動態內容: {finish.inner_text()}")
    print("載入提示已消失")
    browser.close()
