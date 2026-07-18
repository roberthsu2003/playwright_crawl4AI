# 專案 05：線上書店資料擷取

這是[第 05 章：資料擷取](../../課程章節/第05章_資料擷取/README.md)的對應實戰。擷取 Books to Scrape 前三頁的書名、價格、庫存、評分與連結，先回傳結構化資料。

## 學習重點

- 處理多個 locator 與重複元素
- `inner_text()` 與 `get_attribute()`
- 相對連結轉成完整 URL
- 分頁與結構化 `list[dict]` 回傳值

## 完成步驟

1. 手動瀏覽 Books to Scrape 前兩頁，確認商品卡、Next 與相對連結的位置。
2. 開啟 [`main.py`](main.py)，閱讀 `scrape_books()` 的分頁迴圈與欄位擷取。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案05_線上書店資料擷取/main.py
```

4. 觀察每頁累計筆數，以及最後顯示的前三筆字典資料。
5. 驗收總數為 60，且每筆都有 `title`、`price`、`stock`、`rating`、`url`。
6. 先能解釋資料如何從網頁進入 `list[dict]`，再複製 AI Prompt 加入儀表板與檔案匯出。

## 資料儲存判斷

**推薦儲存。**書籍清單適合下載、篩選及交給試算表分析，但儲存不放在爬蟲核心。AI 賦能階段加入 CSV 與 XLSX 匯出即可；本專案不需要資料庫。

## AI 介面升級

[複製 Prompt 05：使用 Dash 製作書店資料儀表板 →](../AI介面設計Prompt.md#prompt-05)

[← 返回第 05 章](../../課程章節/第05章_資料擷取/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
