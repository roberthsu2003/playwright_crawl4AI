from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    requests = []

    page.on("request", lambda req: requests.append({"url": req.url, "method": req.method}))

    page.on("response", lambda resp: print(
        f"[{resp.status}] {resp.request.method} {resp.url[:80]}"
    ) if "zh.wikipedia.org" in resp.url else None)

    page.goto("https://zh.wikipedia.org/wiki/臺灣", timeout=15000)
    page.wait_for_load_state("domcontentloaded")

    print(f"\n總共發送 {len(requests)} 個請求")
    print(f"GET 請求: {sum(1 for r in requests if r['method'] == 'GET')}")
    print(f"其他請求: {sum(1 for r in requests if r['method'] != 'GET')}")

    image_reqs = [r for r in requests if any(e in r['url'] for e in ['.png', '.jpg', '.svg', '.gif'])]
    print(f"圖片請求: {len(image_reqs)} 個")

    browser.close()
