# 專案 05：線上書店資料擷取

這是[第 05 章：資料擷取](../../課程章節/第05章_資料擷取/README.md)的對應實戰。擷取 Books to Scrape 前三頁的書名、價格、庫存、評分與連結，輸出成 CSV。

## 學習重點

- 處理多個 locator 與重複元素
- `inner_text()` 與 `get_attribute()`
- 相對連結轉成完整 URL
- 分頁與 UTF-8 CSV 輸出

## 執行

```bash
uv run python playwright/實戰專案/專案05_線上書店資料擷取/main.py
```

成果為 `output/books.csv`。驗收時確認共有 60 筆資料，且欄位可在試算表正常顯示。

## AI 介面升級

[複製 Prompt 05：使用 Dash 製作書店資料儀表板 →](../AI介面設計Prompt.md#prompt-05)

[← 返回第 05 章](../../課程章節/第05章_資料擷取/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
