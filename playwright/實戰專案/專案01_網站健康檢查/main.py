"""專案 01：開啟真實網頁，檢查標題並留下截圖。"""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


URL = "https://example.com/"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def check_website(browser_name: str = "chromium") -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_name)
        browser = browser_type.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        response = page.goto(URL, wait_until="domcontentloaded")
        heading = page.get_by_role("heading", name="Example Domain").inner_text()
        screenshot = OUTPUT_DIR / f"homepage_{browser_name}.png"
        page.screenshot(path=screenshot, full_page=True)

        print(f"瀏覽器: {browser_name}")
        print(f"HTTP 狀態: {response.status if response else '無回應'}")
        print(f"頁面標題: {page.title()}")
        print(f"主標題: {heading}")
        print(f"截圖: {screenshot}")
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--browser", choices=["chromium", "firefox", "webkit"], default="chromium"
    )
    args = parser.parse_args()
    check_website(args.browser)
