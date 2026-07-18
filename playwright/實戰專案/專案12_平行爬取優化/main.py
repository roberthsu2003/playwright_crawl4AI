"""專案 12：以 async Playwright 平行擷取三個書籍類別並比較耗時。"""

import asyncio
import time

from playwright.async_api import Browser, Page, Route, async_playwright


CATEGORIES = {
    "Travel": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "Mystery": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "Historical Fiction": "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
}
async def block_heavy_resources(route: Route) -> None:
    if route.request.resource_type in {"image", "font", "media"}:
        await route.abort()
    else:
        await route.continue_()


async def open_with_retry(page: Page, url: str, attempts: int = 3) -> None:
    for attempt in range(1, attempts + 1):
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15_000)
            return
        except Exception:
            if attempt == attempts:
                raise
            await asyncio.sleep(attempt)


async def scrape_category(browser: Browser, category: str, url: str) -> list[dict[str, str]]:
    context = await browser.new_context()
    page = await context.new_page()
    await page.route("**/*", block_heavy_resources)
    try:
        await open_with_retry(page, url)
        await page.locator("article.product_pod").first.wait_for()
        books: list[dict[str, str]] = []
        for item in await page.locator("article.product_pod").all():
            link = item.locator("h3 a")
            books.append(
                {
                    "category": category,
                    "title": await link.get_attribute("title") or "",
                    "price": await item.locator(".price_color").inner_text(),
                }
            )
        print(f"{category}: {len(books)} 本")
        return books
    finally:
        await context.close()


async def main() -> None:
    start = time.perf_counter()
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        results = await asyncio.gather(
            *(scrape_category(browser, name, url) for name, url in CATEGORIES.items())
        )
        await browser.close()

    books = [book for category_books in results for book in category_books]
    elapsed = time.perf_counter() - start
    print(f"共 {len(books)} 本 / {elapsed:.2f} 秒")
    for book in books[:3]:
        print(book)
    print("目前只顯示前三筆；效能紀錄儲存將在 AI 賦能階段加入。")


if __name__ == "__main__":
    asyncio.run(main())
