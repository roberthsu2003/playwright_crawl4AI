"""專案 10：登入 SauceDemo，儲存狀態後在新 context 重複使用。"""

import re

from pathlib import Path

from playwright.sync_api import expect, sync_playwright


LOGIN_URL = "https://www.saucedemo.com/"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
AUTH_FILE = OUTPUT_DIR / "auth.json"


with sync_playwright() as playwright:
    OUTPUT_DIR.mkdir(exist_ok=True)
    browser = playwright.chromium.launch(headless=True)

    first_context = browser.new_context()
    page = first_context.new_page()
    page.goto(LOGIN_URL)
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))

    first_context.storage_state(path=AUTH_FILE)
    print(f"已儲存狀態: {AUTH_FILE}")
    first_context.close()

    second_context = browser.new_context(storage_state=AUTH_FILE)
    restored_page = second_context.new_page()
    restored_page.goto("https://www.saucedemo.com/inventory.html")
    expect(restored_page).to_have_url(re.compile(r".*/inventory\.html$"))

    local_storage = restored_page.evaluate("Object.keys(localStorage)")
    cookies = second_context.cookies()
    print(f"未再輸入密碼，直接開啟: {restored_page.title()}")
    print(f"Cookie 數量: {len(cookies)} / localStorage keys: {local_storage}")

    second_context.close()
    browser.close()
