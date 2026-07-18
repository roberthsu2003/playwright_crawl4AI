# 專案 12：平行爬取優化

這是[第 12 章：效能優化](../../課程章節/第12章_效能優化/README.md)的對應實戰。使用 async Playwright 平行擷取 Books to Scrape 三個類別，同時擋截大型資源並加入重試。

## 學習重點

- `async_playwright` 與 `asyncio.gather()`
- 每個平行任務使用獨立 browser context
- route 阻擋圖片、字型與媒體
- timeout、重試、`finally` 清理與效能計時

## 完成步驟

1. 先完成 [Asyncio 非同步編程](../../../基礎課程/asyncio/) 的基本概念。
2. 開啟 [`main.py`](main.py)，找出 `asyncio.gather()`、獨立 context、route 擋資源、重試與 `finally`。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案12_平行爬取優化/main.py
```

4. 觀察三個類別的筆數、總筆數、耗時與前三筆資料。
5. 驗收 Travel、Mystery、Historical Fiction 都成功，瀏覽器與 context 都正常關閉。
6. 先手動記下本次耗時，再使用 AI Prompt 建立可重複比較的效能儀表板。

## 資料儲存判斷

**推薦儲存實驗摘要，不必保存全部書籍。**AI 賦能階段可用 CSV 匯出比較表，或用 SQLite 保存多次 benchmark（時間、並行數、成功率、重試數）；不使用雲端資料庫。

## AI 介面升級

[複製 Prompt 12：使用 Dash 製作平行爬取效能儀表板 →](../AI介面設計Prompt.md#prompt-12)

[← 返回第 12 章](../../課程章節/第12章_效能優化/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
