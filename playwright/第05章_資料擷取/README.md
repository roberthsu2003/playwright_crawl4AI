# 第五章：資料擷取

學習如何從網頁中提取所需的資料。

## 5.1 獲取元素內容

### `inner_text()` - 取得文字內容

```python
# 取得可見文字（類似使用者看到的）
text = page.locator("#title").inner_text()
print(text)

# 範例
page.goto("https://example.com")
title = page.locator("h1").inner_text()
```

### `text_content()` - 取得所有文字

```python
# 取得所有文字（包含隱藏元素）
text = page.locator("#content").text_content()

# inner_text() vs text_content()
# inner_text(): 只取可見文字，考慮 CSS 樣式
# text_content(): 取所有文字，不考慮樣式
```

### `inner_html()` - 取得 HTML 內容

```python
# 取得元素的 HTML 內容
html = page.locator("#article").inner_html()
print(html)

# 取得包含元素本身的 HTML
html = page.eval_on_selector("#article", "el => el.outerHTML")
```

---

## 5.2 獲取屬性值

### `get_attribute()` - 取得元素屬性

```python
# 取得連結的 href
href = page.locator("a#link").get_attribute("href")

# 取得圖片的 src
src = page.locator("img#logo").get_attribute("src")

# 取得 data 屬性
data_id = page.locator("div").get_attribute("data-id")

# 取得 class
class_name = page.locator("button").get_attribute("class")
```

### 常用屬性

```python
# href - 連結網址
link_url = page.locator("a").get_attribute("href")

# src - 圖片/腳本來源
image_url = page.locator("img").get_attribute("src")

# value - 輸入框的值
input_value = page.locator("input").get_attribute("value")

# alt - 圖片替代文字
alt_text = page.locator("img").get_attribute("alt")

# title - 標題屬性
title = page.locator("a").get_attribute("title")
```

---

## 5.3 處理多個元素

### `query_selector_all()` - 取得所有符合的元素

```python
# 方法1：使用 locator.all()
items = page.locator("div.item").all()
for item in items:
    print(item.inner_text())

# 方法2：使用 element_handles
items = page.query_selector_all("div.item")
for item in items:
    print(item.inner_text())
```

### 迴圈處理元素列表

```python
# 取得所有商品名稱
products = page.locator("div.product h3").all()
for product in products:
    name = product.inner_text()
    print(f"商品: {name}")

# 取得所有連結
links = page.locator("a").all()
for link in links:
    url = link.get_attribute("href")
    text = link.inner_text()
    print(f"{text}: {url}")
```

### 批量資料擷取

```python
# 取得商品列表資料
products_data = []
products = page.locator("div.product").all()

for product in products:
    data = {
        "name": product.locator("h3").inner_text(),
        "price": product.locator(".price").inner_text(),
        "image": product.locator("img").get_attribute("src")
    }
    products_data.append(data)

print(products_data)
```

---

## 5.4 實作：爬取商品列表

### 實際案例：電商網站商品資訊

```python
from playwright.sync_api import sync_playwright
import json

def scrape_products():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 訪問商品列表頁
        page.goto("https://example-shop.com/products")
        
        # 等待商品載入
        page.wait_for_selector("div.product-card")
        
        # 儲存商品資料
        products = []
        
        # 取得所有商品卡片
        product_cards = page.locator("div.product-card").all()
        
        for card in product_cards:
            try:
                product = {
                    "name": card.locator("h2.title").inner_text(),
                    "price": card.locator("span.price").inner_text(),
                    "rating": card.locator("div.rating").inner_text(),
                    "image": card.locator("img").get_attribute("src"),
                    "link": card.locator("a").get_attribute("href")
                }
                products.append(product)
            except Exception as e:
                print(f"擷取商品失敗: {e}")
                continue
        
        # 儲存為 JSON
        with open("products.json", "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print(f"成功擷取 {len(products)} 個商品")
        
        browser.close()

if __name__ == "__main__":
    scrape_products()
```

### 進階：分頁擷取

```python
def scrape_multiple_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        all_products = []
        
        # 爬取前 3 頁
        for page_num in range(1, 4):
            url = f"https://example-shop.com/products?page={page_num}"
            page.goto(url)
            page.wait_for_selector("div.product-card")
            
            # 擷取當前頁面商品
            products = page.locator("div.product-card").all()
            for product in products:
                data = {
                    "name": product.locator("h2").inner_text(),
                    "price": product.locator(".price").inner_text()
                }
                all_products.append(data)
            
            print(f"第 {page_num} 頁：擷取 {len(products)} 個商品")
        
        print(f"總共擷取 {len(all_products)} 個商品")
        browser.close()

if __name__ == "__main__":
    scrape_multiple_pages()
```

---

## 完整範例：爬取新聞標題

### 本地測試檔案

本章提供完整的本地測試環境：

- **[`news_sample.html`](./news_sample.html)** - 新聞網站範例頁面
- **[`scrape_news.py`](./scrape_news.py)** - 新聞爬蟲程式

### 執行方式

```bash
# 進入第05章目錄
cd playwright/第05章_資料擷取

# 執行爬蟲程式
python scrape_news.py
```

### 程式碼說明

```python
from playwright.sync_api import sync_playwright
import csv
import json
from pathlib import Path

def scrape_news():
    """爬取本地新聞網站範例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 取得當前檔案的絕對路徑
        current_dir = Path(__file__).parent
        html_file = current_dir / "news_sample.html"
        
        # 訪問本地 HTML 檔案
        page.goto(f"file://{html_file.absolute()}")
        
        # 等待新聞項目載入
        page.wait_for_selector("article.news-item")
        
        news_list = []
        articles = page.locator("article.news-item").all()
        
        for article in articles:
            news = {
                "title": article.locator("h2").inner_text(),
                "summary": article.locator("p.summary").inner_text(),
                "time": article.locator("time").inner_text(),
                "category": article.locator(".category").inner_text(),
                "link": article.locator("a").get_attribute("href")
            }
            news_list.append(news)
        
        # 儲存為 CSV
        csv_file = current_dir / "news.csv"
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "summary", "time", "category", "link"])
            writer.writeheader()
            writer.writerows(news_list)
        
        # 儲存為 JSON
        json_file = current_dir / "news.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        print(f"總共成功擷取 {len(news_list)} 則新聞")
        browser.close()

if __name__ == "__main__":
    scrape_news()
```

### 執行結果

程式會產生兩個檔案：

1. `news.csv` - CSV 格式的新聞資料
2. `news.json` - JSON 格式的新聞資料

### 學習重點

- 使用 `Path` 處理檔案路徑
- 爬取本地 HTML 檔案進行測試
- 同時輸出 CSV 和 JSON 兩種格式
- 處理多個元素的資料擷取
- 錯誤處理與資料驗證

---

## 🌐 真實網站範例：爬取書籍資料

使用 `books.toscrape.com`（專為爬蟲設計的練習網站）示範批量資料擷取。

```python
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
```

**執行方式：**
```bash
uv run python playwright/第05章_資料擷取/real_example.py
```

---

## 練習題

1. 爬取一個新聞網站的標題和連結
2. 擷取電商網站的商品資訊（名稱、價格、圖片）
3. 練習使用 `inner_text()` 和 `text_content()` 的差異
4. 將擷取的資料儲存為 JSON 或 CSV 檔案

---

[← 上一章：等待與同步](../第04章_等待與同步/README.md) | [返回目錄](../README.md) | [下一章：進階互動 →](../第06章_進階互動/README.md)
