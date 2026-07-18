"""專案 09：監聽 JSONPlaceholder API，並將同一請求改成 Mock 回應。"""

import json

from playwright.sync_api import sync_playwright


HOME_URL = "https://jsonplaceholder.typicode.com/"
API_PATTERN = "**/posts/1"


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    page.on(
        "request",
        lambda request: print(f"請求: {request.method} {request.url}")
        if "/posts/1" in request.url
        else None,
    )
    page.goto(HOME_URL, wait_until="domcontentloaded")

    with page.expect_response(lambda response: "/posts/1" in response.url) as response_info:
        real_data = page.evaluate("async () => (await fetch('/posts/1')).json()")
    response = response_info.value
    print(f"真實回應: HTTP {response.status} / {real_data['title']}")

    mock_data = {"userId": 99, "id": 1, "title": "教室 Mock 資料", "body": "Playwright route"}
    page.route(
        API_PATTERN,
        lambda route: route.fulfill(
            status=200,
            content_type="application/json; charset=utf-8",
            body=json.dumps(mock_data, ensure_ascii=False),
        ),
    )
    mocked = page.evaluate("async () => (await fetch('/posts/1')).json()")
    print(f"Mock 回應: {mocked['title']} / {mocked['body']}")

    browser.close()
