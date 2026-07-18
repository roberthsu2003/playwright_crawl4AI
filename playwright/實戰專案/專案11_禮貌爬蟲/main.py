"""專案 11：用透明身分、合理視窗與限速建立禮貌爬蟲。"""

import json

from playwright.sync_api import sync_playwright


HEADERS_URL = "https://httpbingo.org/headers"
ROBOTS_URL = "https://httpbingo.org/robots.txt"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="PlaywrightCourseBot/1.0 (+classroom@example.invalid)",
        viewport={"width": 1366, "height": 768},
        locale="zh-TW",
        timezone_id="Asia/Taipei",
        extra_http_headers={"Accept-Language": "zh-TW,zh;q=0.9,en;q=0.7"},
    )
    page = context.new_page()

    page.goto(ROBOTS_URL, wait_until="domcontentloaded")
    robots_text = page.locator("body").inner_text()
    print("robots.txt:\n" + robots_text.strip())

    # 教學範例主動降速；實務應依網站規範設定更長間隔。
    page.wait_for_timeout(1_200)
    page.goto(HEADERS_URL, wait_until="domcontentloaded")
    data = json.loads(page.locator("body").inner_text())
    headers = data["headers"]

    print(f"User-Agent: {headers.get('User-Agent')}")
    print(f"Accept-Language: {headers.get('Accept-Language')}")
    print(f"視窗: {page.viewport_size}")
    print("原則：不繞過 CAPTCHA、不隱藏身分、不高頻請求。")

    context.close()
    browser.close()
