"""專案 08：將 Wikipedia 頁面製作成截圖、錄影與 PDF 報告。"""

from pathlib import Path

from playwright.sync_api import sync_playwright


URL = "https://zh.wikipedia.org/wiki/Playwright_(軟體)"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


with sync_playwright() as playwright:
    OUTPUT_DIR.mkdir(exist_ok=True)
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        record_video_dir=OUTPUT_DIR / "video",
    )
    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.locator("#firstHeading").wait_for()

    page.screenshot(path=OUTPUT_DIR / "full_page.png", full_page=True)
    page.locator("#firstHeading").screenshot(path=OUTPUT_DIR / "heading.png")
    page.screenshot(
        path=OUTPUT_DIR / "top_area.png",
        clip={"x": 0, "y": 0, "width": 1200, "height": 700},
    )
    page.pdf(
        path=OUTPUT_DIR / "article.pdf",
        format="A4",
        print_background=True,
        margin={"top": "15mm", "right": "12mm", "bottom": "15mm", "left": "12mm"},
    )

    print(f"已產生截圖與 PDF: {OUTPUT_DIR}")
    page.close()  # 關閉 page 後錄影才會完整寫入。
    context.close()
    browser.close()
    print(f"錄影目錄: {OUTPUT_DIR / 'video'}")
