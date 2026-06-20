from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=False)
        
        # 開啟新分頁
        page = browser.new_page()
        
        # 訪問網站
        page.goto("https://www.google.com")
        
        # 取得標題
        print(page.title())
        
        # 關閉瀏覽器
        browser.close()

if __name__ == "__main__":
    run()