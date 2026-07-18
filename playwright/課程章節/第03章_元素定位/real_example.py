from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)

    print("=== CSS 選擇器 ===")
    titles = page.locator("div.title a").all()
    for t in titles[:3]:
        print(f"  {t.inner_text()}")

    print("\n=== get_by_role ===")
    links = page.get_by_role("link").all()
    count = 0
    for link in links:
        text = link.inner_text().strip()
        if text:
            print(f"  {text}")
            count += 1
            if count >= 3:
                break

    print("\n=== XPath ===")
    xpath_titles = page.locator("//div[@class='title']/a").all()
    for t in xpath_titles[:3]:
        print(f"  {t.inner_text()}")

    print("\n=== 取得連結屬性 ===")
    for t in titles[:3]:
        href = t.get_attribute("href")
        print(f"  {t.inner_text()} -> {href}")

    browser.close()
