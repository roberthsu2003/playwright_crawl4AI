# 專案 01：網站健康檢查

這是[第 01 章：Playwright 簡介](../../課程章節/第01章_Playwright簡介/README.md)的對應實戰。使用真實瀏覽器開啟 Example Domain，檢查 HTTP 狀態、頁面標題與主標題，並儲存截圖。

## 學習重點

- 啟動 Chromium、Firefox 或 WebKit
- `page.goto()`、`page.title()` 與 role locator
- HTTP 回應狀態與整頁截圖
- 使用命令列參數切換瀏覽器

## 執行

```bash
uv run python playwright/實戰專案/專案01_網站健康檢查/main.py
uv run python playwright/實戰專案/專案01_網站健康檢查/main.py --browser firefox
```

成果會儲存在本目錄的 `output/`。驗收時確認 HTTP 為 200、標題為 Example Domain，且截圖可正常開啟。

## AI 介面升級

[複製 Prompt 01：使用 tkinter 製作網站健康檢查桌面 App →](../AI介面設計Prompt.md#prompt-01)

[← 返回第 01 章](../../課程章節/第01章_Playwright簡介/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
