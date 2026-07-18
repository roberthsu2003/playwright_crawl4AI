from playwright.sync_api import sync_playwright
from pathlib import Path

out_dir = Path("output")
out_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("=== 全頁截圖 ===")
    page.goto("https://zh.wikipedia.org/wiki/臺灣", timeout=15000)
    page.wait_for_load_state("domcontentloaded")
    page.screenshot(path=str(out_dir / "wikipedia_full.png"), full_page=True)
    print("已儲存: wikipedia_full.png")

    print("\n=== 元素截圖 ===")
    heading = page.locator("#firstHeading")
    heading.screenshot(path=str(out_dir / "heading.png"))
    print(f"已儲存: heading.png ({heading.inner_text()})")

    print("\n=== 資訊框截圖 ===")
    info_box = page.locator("table.infobox").first
    info_box.screenshot(path=str(out_dir / "infobox.png"))
    print("已儲存: infobox.png")

    browser.close()
