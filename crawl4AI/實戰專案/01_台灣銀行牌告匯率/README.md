# 專案 01：台灣銀行牌告匯率

使用 Crawl4AI 擷取[台灣銀行牌告匯率](https://rate.bot.com.tw/xrt?Lang=zh-TW)，把表格轉成結構化 `list[dict]`。課堂版本只執行一次並顯示資料，讓學習焦點留在 CSS Schema、非同步爬取與結果驗證。

## 完成後你會學會

- 使用 `JsonCssExtractionStrategy` 定義表格欄位
- 使用 `AsyncWebCrawler` 與 `await crawler.arun()`
- 解析 `result.extracted_content`
- 檢查 `result.success` 與錯誤訊息
- 判斷何時值得保存資料

## 前置準備

1. 先完成 [Asyncio 非同步編程](../../../基礎課程/asyncio/)。
2. 在 repo 根目錄執行：

```bash
uv sync
uv run crawl4ai-setup
```

## 專案檔案

```text
01_台灣銀行牌告匯率/
├── main.py       # Crawl4AI 核心爬蟲
└── README.md     # 本操作說明
```

## 完成步驟

1. 用瀏覽器開啟目標網站，找到牌告匯率表格，觀察每列的 `data-table` 屬性。
2. 開啟 [`main.py`](main.py)，閱讀 `schema` 的 `baseSelector` 與五個 `fields`。
3. 確認 `CrawlerRunConfig` 使用 `JsonCssExtractionStrategy`，並在失敗時先處理 `result.error_message`。
4. 從 repo 根目錄執行：

```bash
uv run python crawl4AI/實戰專案/01_台灣銀行牌告匯率/main.py
```

5. 在輸出中找到幣名、現金買入／賣出、即期買入／賣出。
6. 將其中一個 selector 暫時改錯，觀察空資料或失敗狀態後還原。
7. 能說明「網頁列 → Schema → JSON 字串 → Python list」的流程後，再進行 AI 賦能。

## 驗收清單

- [ ] 程式只執行一次後正常結束，不需要用 Ctrl+C 停止。
- [ ] `result.success` 為成功，且有多種幣別。
- [ ] 每筆資料包含五個預期欄位。
- [ ] 程式沒有建立 JSON、CSV、XLSX 或資料庫。
- [ ] 我能指出至少一個 CSS selector 對應的網頁欄位。

## 資料儲存判斷

**適合保存歷史，但不在爬蟲核心實作。**單次匯率只看畫面即可；要比較不同時間的變化時，才由 AI 加入本機 SQLite。每次執行以「擷取時間 + 幣別」保存一筆快照，適合查詢趨勢，也避免產生大量零散檔案。

[複製 AI Prompt 01：加入 SQLite 匯率歷史與介面 →](../AI資料儲存Prompt.md#prompt-01)

## 常見問題

### 沒有資料

先在瀏覽器確認網站可開啟，再檢查 HTML 屬性是否改版。不要直接增加長時間等待，應先確認 selector。

### `crawl4ai-setup` 找不到

確認已在 repo 根目錄執行 `uv sync`；也可依目前 Crawl4AI 版本的安裝訊息完成瀏覽器設定。

[返回實戰專案總覽](../README.md) | [主程式](main.py)
