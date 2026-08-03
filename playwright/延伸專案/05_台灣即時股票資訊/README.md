# 專案 05：台灣即時股票資訊 (Playwright 版)

使用 **Playwright** 擷取台灣股市的即時股票行情數據，學習動態 DOM 元素定位、自動化網頁載入等待以及即時資料結構化處理。

---

## 🎯 完成後你會學會

- 使用 Playwright 啟動與配置 `Browser` / `BrowserContext`
- 自動開啟目標股票行情網頁並等待動態 DOM 渲染
- 使用語意化與 CSS Selector 定位即時股價、漲跌幅度與行情細節
- 將擷取到的非結構化網頁資料轉為乾淨的 Python `dict`
- 在終端機 (Console) 格式化印出可讀性極佳的即時報表 (預設無 GUI)

---

## 📌 專案設計理念（無 GUI 說明）

本專案專注於**核心爬蟲技術**與 Playwright 自動化原理教學。
- **不加入 GUI 介面**：現代開發流程中，UI/GUI 介面可透過 AI 輔助 (Vibe Coding) 快速產生；核心重點是理解網頁元素定位與資料提取。
- **預設不保存資料**：即時股票數值極快過期，核心程式以終端顯示為主。如需導出 CSV 或整合資料庫，可另行擴充。

---

## 🔧 前置準備

1. 確認已安裝 Python 3.11+ 與 `playwright` 套件。
2. 在專案目錄安裝 Playwright Chromium 瀏覽器：

```bash
uv sync
uv run playwright install chromium
```

---

## 📂 專案結構

```text
05_台灣即時股票資訊/
├── main.py       # Playwright 即時股票爬蟲主程式
└── README.md     # 專案說明文件
```

---

## 🚀 使用方法

### 1. 預設查詢 (台積電 2330)

移動至專案目錄並執行：

```bash
cd "playwright/延伸專案/05_台灣即時股票資訊"
uv run python main.py
```

### 2. 查詢其他股票代碼

可在命令列傳入欲查詢的股票代碼（例如鴻海 `2317` 或聯發科 `2454`）：

```bash
uv run python main.py 2317
```

---

## 🖥️ 終端機報表輸出範例

```text
============================================================
📊 台灣即時股票資訊報表 - [台積電] (2330)
============================================================
📈 即時成交價 : 2,380
💹 漲跌金額/幅: 45.00
🕒 資料更新時間: 2026/08/03 10:39
------------------------------------------------------------
🔓 開盤價 : 2,390           🔒 昨收價 : 2,425
🔺 最高價 : 2,395           🔻 最低價 : 2,365
============================================================
💡 提示：本數據僅供教學示範與即時顯示，核心程式不預設儲存歷史庫。
```

---

## 📖 核心程式碼解析

```python
async def fetch_stock_quote(stock_code: str = "2330") -> dict:
    url = f"https://tw.stock.yahoo.com/quote/{stock_code}.TW"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)..."
        )
        page = await context.new_page()
        
        # 1. 導航至網頁並等待載入
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_selector("h1", timeout=10000)
        
        # 2. 定位動態股價與標題
        stock_name = (await page.locator("h1").all_inner_texts())[1]
        price = await page.locator("span[class*='Fz(32px)']").first.inner_text()
        
        # 3. 回傳結構化資料
        return {
            "股票代碼": stock_code,
            "股票名稱": stock_name,
            "即時價格": price
        }
```

---

## ✅ 驗收清單

- [x] 瀏覽器能開啟並完成動態內容載入。
- [x] 終端機能正常顯示股票名稱、代碼、即時價格與時間。
- [x] 傳入無效或不同的股票代碼時有良好的錯誤處理。
- [x] 核心程式無任何 GUI 依賴。

---

[← 返回 Playwright 延伸專案目錄](../README.md)
