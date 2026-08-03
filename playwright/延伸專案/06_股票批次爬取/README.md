# 專案 06：股票批次爬取 (Playwright Async 版 - 無 GUI)

使用 **Async Playwright** 與 `asyncio` 併發控制，對台灣股市多支股票進行高效率批次即時行情爬取。本專案包含 CLI 互動式搜尋與批次 CSV / JSON 匯出功能。

---

## 🎯 完成後你會學會

- 使用 Playwright 非同步 API (`async_playwright`) 與 `asyncio` 進行非同步網頁操作
- 使用 `asyncio.Semaphore` 實現**併行數量限制 (Max Concurrency)** 與**速率限制 (Rate Limiting)**
- 整合 `twstock` 實現命令列 (CLI) 股票名稱與代碼搜尋過濾
- 批次整理結構化數據，並在終端機輸出排版對齊的行情報表
- 匯出批次數據為 `CSV` (`utf-8-sig`) 與 `JSON` 檔案

---

## 📌 專案設計理念（無 GUI 說明）

本專案衍生自 `crawl4AI/實戰專案/03_股票批次爬取_GUI`，但**完全移除了所有 GUI (tkinter) 介面程式碼**。
- **核心功能極簡化**：專注於非同步併發爬取演算法、流量控制與數據匯出。
- **CLI 互動介面**：使用乾淨文字選單供學生練習操作。
- **未來擴充性**：後續若需要 UI 介面，學生可透過 Vibe Coding 工具 (如 Gemini / ChatGPT) 快速產生 GUI，並直接串接本專案的核心模組 `stock_batch_scraper.py`。

---

## 🔧 前置準備

1. 在專案根目錄確認已透過 `uv` 安裝依賴套件（包含 `twstock` 與 `playwright`）：

```bash
uv sync
uv run playwright install chromium
```

---

## 📂 專案結構

```text
06_股票批次爬取/
├── stock_batch_scraper.py   # Async Playwright 批次爬蟲核心與匯出模組
├── main.py                  # CLI 選單入口與命令列執行檔
├── README.md                # 專案說明文件
└── output/                  # 執行匯出後自動建立的報表目錄
    ├── stocks_batch.csv
    └── stocks_batch.json
```

---

## 🚀 使用方法

### 1. 啟動 CLI 互動式選單

移動至專案目錄並執行：

```bash
cd "playwright/延伸專案/06_股票批次爬取"
uv run python main.py
```

進入主選單後，可選擇：
- **`[1]`** 預設熱門股票批次抓取 (如 2330, 2317, 2454, 2308, 3008)
- **`[2]`** 使用 `twstock` 進行關鍵字搜尋與選取 (例如輸入 `晶圓` 或 `23`)
- **`[3]`** 自訂股票代碼清單 (輸入以逗號分隔之代碼)
- **`[4]`** 匯出最後一次爬取結果 (CSV / JSON)
- **`[0]`** 離開系統

### 2. 命令列快速批次執行

亦可直接在命令列傳入欲抓取的一或多支股票代碼：

```bash
uv run python main.py 2330 2317 2454 2308
```

---

## 🖥️ 終端機批次報表輸出範例

```text
🚀 開始批次爬取 3 支股票: 2330, 2317, 2454
⏳ [併行抓取中] 股票代碼: 2330 ...
⏳ [併行抓取中] 股票代碼: 2317 ...
⏳ [併行抓取中] 股票代碼: 2454 ...

✨ 批次爬取完成！總耗時: 2.20 秒

==========================================================================================
股票代碼       股票名稱         即時價格         漲跌金額/幅度          資料更新時間              
------------------------------------------------------------------------------------------
2330       台積電          2,380        45.00            2026/08/03 10:40    
2317       鴻海           250.5        0.00             2026/08/03 10:40    
2454       聯發科          3,910        355.00           2026/08/03 10:40    
==========================================================================================

✅ 資料已成功匯出至 CSV 檔案: output/stocks_batch.csv
```

---

## 💡 核心技術重點

### 1. 非同步 Semaphore 速率與併發控制

```python
semaphore = asyncio.Semaphore(max_concurrency)

async def worker(code: str):
    async with semaphore:
        data = await fetch_single_stock(context, code)
        await asyncio.sleep(0.5) # 間隔保護目標伺服器
        return data

tasks = [worker(code) for code in stock_codes]
results = await asyncio.gather(*tasks)
```

### 2. 模組化設計與 Vibe Coding 接軌

`stock_batch_scraper.py` 中的 `batch_fetch_stocks()` 回傳標準 `list[dict]` 結構，可直接與任何 UI 框架（如 Tkinter, PyQt, Streamlit, Web UI）無縫整合。

---

## ✅ 驗收清單

- [x] CLI 介面能正常啟動與引導選單操作。
- [x] 能依股票關鍵字正確搜尋與選取多支股票。
- [x] 使用 `asyncio.Semaphore` 實現非同步併發抓取，3 支股票抓取時間小於 3 秒。
- [x] 成功將爬取結果匯出為 CSV 與 JSON 報表。
- [x] 全專案無任何 GUI 依賴。

---

[← 返回 Playwright 延伸專案目錄](../README.md)
