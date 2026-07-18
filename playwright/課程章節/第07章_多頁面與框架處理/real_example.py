from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)

    article_links = page.locator("div.title a").all()
    links = [a.get_attribute("href") for a in article_links[:3]]
    print(f"將開啟 {len(links)} 個分頁")

    pages = []
    for link in links:
        new_page = context.new_page()
        new_page.goto(f"https://www.ptt.cc{link}")
        pages.append(new_page)
        print(f"已開啟: {new_page.title()}")

    print(f"\n目前有 {len(context.pages)} 個分頁")

    for i, p in enumerate(pages):
        author = p.locator("span.article-meta-value").first
        print(f"分頁 {i+1} 作者: {author.inner_text() if author.count() else 'N/A'}")
        p.close()

    context.close()
    browser.close()
