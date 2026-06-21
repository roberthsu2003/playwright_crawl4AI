from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")

    books = []
    items = page.locator("article.product_pod").all()
    for item in items:
        book = {
            "title": item.locator("h3 a").get_attribute("title"),
            "price": item.locator("p.price_color").inner_text(),
            "rating": item.locator("p.star-rating").get_attribute("class"),
            "link": item.locator("h3 a").get_attribute("href"),
        }
        books.append(book)

    print(f"找到 {len(books)} 本書")
    for b in books[:5]:
        print(f"  {b['title']} - {b['price']} - {b['rating']}")

    with open("books.json", "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    print("已儲存 books.json")

    browser.close()
