"""專案 06：巡檢 hover、鍵盤、滾動、上傳與下載互動。"""

from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "https://the-internet.herokuapp.com"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


with sync_playwright() as playwright:
    OUTPUT_DIR.mkdir(exist_ok=True)
    upload_file = OUTPUT_DIR / "student_upload.txt"
    upload_file.write_text("Playwright upload practice", encoding="utf-8")

    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(f"{BASE_URL}/hovers")
    first_figure = page.locator(".figure").first
    first_figure.hover()
    caption = first_figure.locator(".figcaption h5")
    caption.wait_for(state="visible")
    print(f"懸停結果: {caption.inner_text()}")

    page.goto(f"{BASE_URL}/key_presses")
    page.locator("body").press("Control+A")
    print(f"鍵盤結果: {page.locator('#result').inner_text()}")

    page.goto(f"{BASE_URL}/large")
    page.locator("table").last.scroll_into_view_if_needed()
    print("已滾動到大型頁面底部目標")

    page.goto(f"{BASE_URL}/upload")
    page.locator("#file-upload").set_input_files(upload_file)
    page.get_by_role("button", name="Upload").click()
    page.get_by_role("heading", name="File Uploaded!").wait_for()
    print(f"已上傳: {page.locator('#uploaded-files').inner_text()}")

    page.goto(f"{BASE_URL}/download")
    first_download = page.locator(".example a").first
    with page.expect_download() as download_info:
        first_download.click()
    download = download_info.value
    saved_path = OUTPUT_DIR / download.suggested_filename
    download.save_as(saved_path)
    print(f"已下載: {saved_path}")

    browser.close()
