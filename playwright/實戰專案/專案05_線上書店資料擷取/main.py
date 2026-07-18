"""專案 05：擷取 Books to Scrape 前三頁並回傳結構化資料。"""

from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


START_URL = "https://books.toscrape.com/"
def scrape_books(max_pages: int = 3) -> list[dict[str, str]]:
    books: list[dict[str, str]] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        current_url = START_URL

        for page_number in range(1, max_pages + 1):
            page.goto(current_url, wait_until="domcontentloaded")
            page.locator("article.product_pod").first.wait_for()

            for item in page.locator("article.product_pod").all():
                link = item.locator("h3 a")
                books.append(
                    {
                        "title": link.get_attribute("title") or "",
                        "price": item.locator(".price_color").inner_text(),
                        "stock": item.locator(".availability").inner_text().strip(),
                        "rating": (
                            item.locator(".star-rating").get_attribute("class") or ""
                        ).replace("star-rating ", ""),
                        "url": urljoin(page.url, link.get_attribute("href") or ""),
                    }
                )

            next_link = page.locator("li.next a")
            print(f"第 {page_number} 頁：累計 {len(books)} 本")
            if page_number == max_pages or next_link.count() == 0:
                break
            current_url = urljoin(page.url, next_link.get_attribute("href") or "")

        browser.close()
    return books


if __name__ == "__main__":
    result = scrape_books()
    print(f"擷取完成：共 {len(result)} 筆資料")
    for book in result[:3]:
        print(book)
    print("目前只顯示前三筆；CSV/XLSX 儲存將在 AI 賦能階段加入。")
