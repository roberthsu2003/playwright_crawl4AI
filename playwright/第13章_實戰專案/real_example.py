from playwright.sync_api import sync_playwright
import csv
import time
from pathlib import Path

def crawl_ptt():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
        page.wait_for_selector("button.btn-big", timeout=10000)
        page.get_by_role("button", name="我同意，我已年滿十八歲").click()
        page.wait_for_selector("div.r-ent", timeout=10000)

        articles = []
        for item in page.locator("div.r-ent").all():
            try:
                title_el = item.locator("div.title a")
                if title_el.count() == 0:
                    continue
                articles.append({
                    "title": title_el.inner_text(),
                    "link": title_el.get_attribute("href"),
                    "author": item.locator("div.author").inner_text(),
                    "date": item.locator("div.date").inner_text(),
                })
            except Exception:
                continue

        browser.close()
        return articles

articles = crawl_ptt()
print(f"共爬取 {len(articles)} 篇文章\n")

for a in articles[:5]:
    print(f"[{a['date']}] {a['author']}: {a['title']}")

csv_path = Path("output/ptt_articles.csv")
csv_path.parent.mkdir(exist_ok=True)
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["title", "link", "author", "date"])
    w.writeheader()
    w.writerows(articles)
print(f"\n已儲存至 {csv_path}")
