# 專案 03：股票批次爬取 GUI

這是由 AI 協助完成的 Crawl4AI + tkinter 桌面專案。學生先讀懂批次爬蟲，再操作既有 GUI，最後才請 AI 加入適合批次資料的本機匯出功能。

![股票批次爬取 GUI](../assets/專案4.png)

## 完成後你會學會

- 用 `arun_many()` 與 dispatcher 批次爬取多個網址
- 用速率限制與最大並行數保護目標網站
- 讓背景執行緒執行 async 爬蟲，不凍結 tkinter
- 搜尋、多選並把 `list[dict]` 顯示在 GUI
- 由 AI 加入 CSV／XLSX 匯出，而不改亂爬蟲核心

## 前置準備

1. 先完成[專案 02](../02_台灣即時股票資訊/README.md)。
2. 在 repo 根目錄執行：

```bash
uv sync
uv run crawl4ai-setup
```

> tkinter 隨一般 Python 安裝提供；若系統沒有 tkinter，請先使用含 Tk 支援的 Python。

## 專案檔案

```text
03_股票批次爬取_GUI/
├── index.py       # CLI／GUI 選單入口
├── wantgoo.py     # Crawl4AI 批次爬蟲核心
├── stock_gui.py   # tkinter 介面
├── PRD.md         # AI 協作需求文件
└── README.md
```

## 完成步驟

1. 開啟 [`wantgoo.py`](wantgoo.py)，找出 URL 批次輸入、dispatcher、rate limiter 與回傳的 `list[dict]`。
2. 開啟 [`stock_gui.py`](stock_gui.py)，找出股票選擇、背景執行緒與 `display_results()`。
3. 先執行選單入口：

```bash
uv run python crawl4AI/實戰專案/03_股票批次爬取_GUI/index.py
```

4. 選擇命令列模式，確認預設股票能顯示結果。
5. 重新執行並選擇 GUI 模式；用代碼或名稱搜尋，先選 2～3 支股票，不要全選所有股票。
6. 按「開始爬取股票資料」，確認執行時畫面仍能回應，完成後右側顯示每支股票結果。
7. 測試沒有選股票時的提示，以及網路失敗時的錯誤訊息。
8. 完成核心驗收後，再複製 AI Prompt 加入本機匯出按鈕。

## 驗收清單

- [ ] CLI 與 GUI 都能啟動。
- [ ] 搜尋可以依股票代碼或名稱過濾。
- [ ] 可選 2～3 支股票並取得結構化結果。
- [ ] 爬取期間 GUI 不會凍結。
- [ ] 沒有選擇與網路錯誤都有清楚提示。
- [ ] AI 賦能前不會自動寫出資料檔。

## 資料儲存判斷

**推薦提供手動匯出。**批次股票是一張當下快照，適合讓使用者按鈕匯出 CSV 或 XLSX，再用試算表分析。預設不自動保存、不用 SQLite，也不使用雲端資料庫；若未按匯出，關閉程式後資料即可消失。

[複製 AI Prompt 03：加入 CSV／XLSX 匯出 →](../AI資料儲存Prompt.md#prompt-03)

## 常見問題

### GUI 沒有回應

確認 Crawl4AI 在 worker thread 中執行，且 widget 更新透過 `root.after()` 回到主執行緒。

### 股票太多導致等待很久

教學時只選少量股票。不要移除速率限制或無限制增加並行數。

[產品需求文件](PRD.md) | [返回實戰專案總覽](../README.md)
