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
        
        print(f"找到 {len(articles)} 則新聞\n")
        
        for index, article in enumerate(articles, 1):
            try:
                news = {
                    "title": article.locator("h2").inner_text(),
                    "summary": article.locator("p.summary").inner_text(),
                    "time": article.locator("time").inner_text(),
                    "category": article.locator(".category").inner_text(),
                    "link": article.locator("a").get_attribute("href")
                }
                news_list.append(news)
                
                # 即時顯示擷取的新聞
                print(f"[{index}] {news['title']}")
                print(f"    分類: {news['category']} | 時間: {news['time']}")
                print(f"    摘要: {news['summary'][:50]}...")
                print()
                
            except Exception as e:
                print(f"擷取第 {index} 則新聞失敗: {e}")
                continue
        
        # 儲存為 CSV
        csv_file = current_dir / "news.csv"
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "summary", "time", "category", "link"])
            writer.writeheader()
            writer.writerows(news_list)
        
        print(f"✅ CSV 檔案已儲存: {csv_file}")
        
        # 儲存為 JSON
        json_file = current_dir / "news.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON 檔案已儲存: {json_file}")
        print(f"\n總共成功擷取 {len(news_list)} 則新聞")
        
        browser.close()

if __name__ == "__main__":
    scrape_news()
