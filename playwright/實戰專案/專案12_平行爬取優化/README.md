# 專案 12：平行爬取優化

這是[第 12 章：效能優化](../../課程章節/第12章_效能優化/README.md)的對應實戰。使用 async Playwright 平行擷取 Books to Scrape 三個類別，同時擋截大型資源並加入重試。

## 學習重點

- `async_playwright` 與 `asyncio.gather()`
- 每個平行任務使用獨立 browser context
- route 阻擋圖片、字型與媒體
- timeout、重試、`finally` 清理與 JSON 輸出

## 執行

```bash
uv run python playwright/實戰專案/專案12_平行爬取優化/main.py
```

成果為 `output/books_parallel.json`。驗收時確認 Travel、Mystery 與 Historical Fiction 都有資料，並記錄總耗時。

## AI 介面升級

[複製 Prompt 12：使用 Dash 製作平行爬取效能儀表板 →](../AI介面設計Prompt.md#prompt-12)

[← 返回第 12 章](../../課程章節/第12章_效能優化/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
