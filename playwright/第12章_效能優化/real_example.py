from playwright.sync_api import sync_playwright
import time

urls = [
    "https://www.ptt.cc/bbs/Gossiping/index.html",
    "https://zh.wikipedia.org/wiki/臺灣",
    "https://books.toscrape.com/",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    print("=== 未優化：依序載入 ===")
    start = time.time()
    for url in urls:
        page = browser.new_page()
        if "ptt.cc" in url:
            page.goto(url)
            page.wait_for_selector("button.btn-big", timeout=10000)
            page.get_by_role("button", name="我同意，我已年滿十八歲").click()
        else:
            page.goto(url)
        page.wait_for_load_state("domcontentloaded")
        print(f"  {page.title()[:30]}...")
        page.close()
    seq_time = time.time() - start
    print(f"依序載入耗時: {seq_time:.1f} 秒\n")

    print("=== 優化：使用 context 禁用資源 ===")
    start = time.time()
    context = browser.new_context()
    page_opt = context.new_page()

    def block_resources(route):
        url = route.request.url
        if any(ext in url for ext in ['.png', '.jpg', '.gif', '.svg', '.woff', '.woff2']):
            route.abort()
        else:
            route.continue_()

    page_opt.route("**/*", block_resources)

    for url in urls:
        if "ptt.cc" in url:
            page_opt.goto(url)
            page_opt.wait_for_selector("button.btn-big", timeout=10000)
            page_opt.get_by_role("button", name="我同意，我已年滿十八歲").click()
        else:
            page_opt.goto(url)
        page_opt.wait_for_load_state("domcontentloaded")
        print(f"  {page_opt.title()[:30]}...")
    context.close()
    opt_time = time.time() - start
    print(f"優化後載入耗時: {opt_time:.1f} 秒")
    print(f"加速比: {seq_time/opt_time:.1f}x")

    browser.close()
