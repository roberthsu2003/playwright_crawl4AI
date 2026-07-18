# 專案 02：台灣即時股票資訊

使用 Crawl4AI 擷取玩股網的台積電技術分析頁，練習 JavaScript 動態內容、CSS Schema 與即時資料驗證。核心程式只在終端顯示本次結果。

**目標網站：**[玩股網台積電技術分析](https://www.wantgoo.com/stock/2330/technical-chart)

## 完成後你會學會

- 設定 `BrowserConfig` 與 `CrawlerRunConfig`
- 在真實瀏覽器等待 JavaScript 渲染
- 用 `js_code` 觸發頁面互動
- 擷取股票代碼、名稱、價格、漲跌與成交量
- 分辨即時顯示與歷史儲存的需求

## 前置準備

1. 完成 [Asyncio 非同步編程](../../../基礎課程/asyncio/)。
2. 在 repo 根目錄執行：

```bash
uv sync
uv run crawl4ai-setup
```

## 完成步驟

1. 手動開啟目標頁，確認股票代碼、名稱、價格與更新時間可見。
2. 開啟 [`main.py`](main.py)，找到 `schema`，逐一對照欄位與 selector。
3. 閱讀 `BrowserConfig(headless=False)`；第一次保留可見瀏覽器以觀察過程。
4. 找出 `js_command` 與 `CrawlerRunConfig` 的 `scan_full_page`、`cache_mode`、`js_code`。
5. 從 repo 根目錄執行：

```bash
uv run python crawl4AI/實戰專案/02_台灣即時股票資訊/main.py
```

6. 確認輸出為結構化資料，且股票號碼為 `2330`。
7. 將 URL 中的股票代碼換成另一支股票測試；完成後還原或清楚註記。

## 驗收清單

- [ ] 瀏覽器能開啟並完成動態內容載入。
- [ ] 終端至少顯示股票代碼、名稱、價格與漲跌資訊。
- [ ] 網路或 selector 失敗時有可讀錯誤。
- [ ] 核心程式不建立資料檔或資料庫。
- [ ] 我能說明 `js_code` 在何時執行。

## 資料儲存判斷

**本專案不需要預設保存。**單一股票的即時值很快過期，介面直接顯示較合適。若學生的延伸目標明確是「比較一段時間的變化」，才由 AI 加入 SQLite；若只要交作業快照，可匯出單次 CSV。

[複製 AI Prompt 02：建立即時股票介面（預設不儲存）→](../AI資料儲存Prompt.md#prompt-02)

## 常見問題

### 欄位是空字串

先檢查網站是否改版，再確認 selector；動態資料尚未出現時，應設定明確等待條件，不用固定長時間 sleep 猜測。

### 網頁拒絕連線或載入很慢

降低執行頻率，稍後再試。不要加入繞過驗證、代理輪替或高頻重試。

[返回實戰專案總覽](../README.md) | [主程式](main.py)
