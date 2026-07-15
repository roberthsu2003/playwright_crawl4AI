# 第一章：Playwright 簡介

## 1.1 什麼是 Playwright？

### Web 自動化測試工具
Playwright 是由 Microsoft 開發的現代化網頁自動化測試框架，支援多種程式語言包括 Python、JavaScript、Java 和 .NET。

### 與 Selenium 的比較
| 特性 | Playwright | Selenium |
|------|-----------|----------|
| 速度 | 更快 | 較慢 |
| API 設計 | 現代化、簡潔 | 較為傳統 |
| 自動等待 | 內建智慧等待 | 需手動設定 |
| 多瀏覽器支援 | Chromium、Firefox、WebKit | Chrome、Firefox、Safari、Edge |
| 網路攔截 | 原生支援 | 需額外工具 |

### Playwright 的優勢
1. **速度快**：使用 CDP (Chrome DevTools Protocol) 直接通訊
2. **支援多瀏覽器**：一套程式碼可在不同瀏覽器執行
3. **更穩定**：內建自動等待機制，減少 flaky tests
4. **功能強大**：支援網路攔截、模擬、截圖、錄影等

> Flaky Test (不穩定測試) 指的是在程式碼和環境都沒有改變的情況下，同一個測試有時候會通過 (Pass)，有時候卻會失敗 (Fail) 的現象。

---

## 1.2 Playwright 的應用場景

### 網頁爬蟲（抓取動態網站資料)
- 處理 JavaScript 渲染的網頁
- 抓取需要登入的網站資料
- 處理無限滾動頁面

> **新手科普**：
> *   **JavaScript 渲染**：現代網站很多內容（如股票報價、動態新聞）是靠程式跑出來的，傳統爬蟲抓不到，但 Playwright 模擬真實瀏覽器，所以抓得到。
> *   **無限滾動**：就像滑 Instagram 或 Facebook，滑到底才會載入新內容，Playwright 可以模擬「一直往下滑」的動作來抓資料。

### 自動化測試
- E2E (End-to-End) 測試
- 功能測試
- 回歸測試

> **新手科普**：
> *   **E2E (端對端) 測試**：模擬真實使用者「從頭到尾」的操作。例如：從「登入」→「選商品」→「加入購物車」→「結帳」，確保整條路都通。
> *   **回歸測試 (Regression Testing)**：當工程師修改程式碼後，重新跑一次測試，確保「新的修改沒有把舊的功能弄壞」。

### 網頁截圖與 PDF 生成
- 自動生成網頁截圖
- 將網頁轉換為 PDF
- 視覺回歸測試

> **新手科普**：
> *   **視覺回歸測試**：電腦自動幫你比對「今天的截圖」和「昨天的截圖」哪裡不一樣。例如按鈕歪了 1 像素，人眼看不出來，但程式抓得出來。

### 表單自動填寫
- 自動化資料輸入
- 批量處理表單
- 重複性操作自動化

> **新手科普**：
> *   這就像是有一個「隱形機器人」幫你操作電腦。例如每天早上要登入後台填寫 100 份報表，人工做要 3 小時，Playwright 可能 3 分鐘就做完了，而且不會手殘打錯字。

---

## 1.3 環境安裝與設定

### Python 環境檢查
```bash
# 檢查 Python 版本（需要 3.8 或以上）
python --version
# 或
python3 --version
```

### 安裝 Playwright
```bash
# 使用 pip 安裝
pip install playwright

# 或使用 pip3
pip3 install playwright
```

### 下載瀏覽器驅動
```bash
# 安裝所有瀏覽器
playwright install

# 只安裝特定瀏覽器
playwright install chromium
playwright install firefox
playwright install webkit
```

### 第一個測試程式
```python
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
```

### 執行程式
```bash
python your_script.py
```

---

## 🌐 真實網站範例：PTT 八卦版

使用 Playwright 開啟 PTT 八卦版，處理年齡確認頁面，擷取文章列表並儲存截圖。

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)
    title = page.title()
    print(f"頁面標題: {title}")

    articles = page.locator("div.r-ent div.title a").all()
    print(f"文章數量: {len(articles)}")
    for article in articles[:5]:
        print(f"  - {article.inner_text()}")

    page.screenshot(path="ptt_screenshot.png", full_page=True)
    print("截圖已儲存: ptt_screenshot.png")
    browser.close()
```

**執行方式：**
```bash
uv run python playwright/第01章_Playwright簡介/real_example.py
```

---

## 練習題

1. 安裝 Playwright 並驗證安裝成功
2. 執行第一個測試程式，訪問你喜歡的網站
3. 修改程式，讓瀏覽器訪問 3 個不同的網站
4. 嘗試使用不同的瀏覽器（Chromium、Firefox、WebKit）

---

## 補充資源

- [Playwright 官方文件](https://playwright.dev/python/)
- [Playwright GitHub](https://github.com/microsoft/playwright-python)
- [Playwright API 參考](https://playwright.dev/python/docs/api/class-playwright)

[← 返回主目錄](../README.md) | [下一章：基礎操作 →](../第02章_基礎操作/README.md)
