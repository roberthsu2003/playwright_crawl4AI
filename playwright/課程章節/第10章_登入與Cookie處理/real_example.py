from playwright.sync_api import sync_playwright
import json
from pathlib import Path

out_dir = Path("output")
out_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    print("=== 第一次訪問：通過年齡確認並儲存 Cookie ===")
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)
    print(f"已進入看板，文章數量: {page.locator('div.title a').count()}")

    cookies = context.cookies()
    with open(out_dir / "ptt_cookies.json", "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"已儲存 {len(cookies)} 個 Cookie")
    context.close()

    print("\n=== 第二次訪問：載入 Cookie，跳過年齡確認 ===")
    with open(out_dir / "ptt_cookies.json", "r") as f:
        saved_cookies = json.load(f)

    context2 = browser.new_context()
    context2.add_cookies(saved_cookies)
    page2 = context2.new_page()
    page2.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page2.wait_for_load_state("domcontentloaded")

    current_url = page2.url
    print(f"當前網址: {current_url}")
    if "over18" not in current_url:
        print("成功！已跳過年齡確認頁面，直接進入看板")
    else:
        print("Cookie 未生效，需要重新確認年齡")

    context2.close()
    browser.close()
