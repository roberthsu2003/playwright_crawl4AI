from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    print("=== 預設瀏覽器指紋 ===")
    default_page = browser.new_page()
    default_page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    agent = default_page.evaluate("navigator.userAgent")
    print(f"User-Agent: {agent[:80]}...")
    webdriver = default_page.evaluate("navigator.webdriver")
    print(f"webdriver: {webdriver}")
    default_page.close()

    print("\n=== 偽裝後的瀏覽器指紋 ===")
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="zh-TW",
        timezone_id="Asia/Taipei",
    )
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    """)

    stealth_page = context.new_page()
    stealth_page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    new_agent = stealth_page.evaluate("navigator.userAgent")
    print(f"User-Agent: {new_agent[:80]}...")
    new_webdriver = stealth_page.evaluate("navigator.webdriver")
    print(f"webdriver: {new_webdriver}")
    languages = stealth_page.evaluate("navigator.languages")
    print(f"languages: {languages}")
    tz = stealth_page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
    print(f"時區: {tz}")

    context.close()
    browser.close()
