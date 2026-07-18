# 專案 01：網站健康檢查

這是[第 01 章：Playwright 簡介](../../課程章節/第01章_Playwright簡介/README.md)的對應實戰。使用真實瀏覽器開啟 Example Domain，檢查 HTTP 狀態、頁面標題與主標題，並儲存截圖。

## 學習重點

- 啟動 Chromium、Firefox 或 WebKit
- `page.goto()`、`page.title()` 與 role locator
- HTTP 回應狀態與整頁截圖
- 使用命令列參數切換瀏覽器

## 完成步驟

1. 先閱讀上方學習重點，再開啟 [`main.py`](main.py)，找到 `page.goto()`、標題定位與 `page.screenshot()`。
2. 在 repo 根目錄完成共用安裝：`uv sync` 與 `uv run playwright install chromium`。
3. 執行 Chromium 版本：

```bash
uv run python playwright/實戰專案/專案01_網站健康檢查/main.py
```

4. 再改用 Firefox 比較結果：

```bash
uv run python playwright/實戰專案/專案01_網站健康檢查/main.py --browser firefox
```

5. 確認終端顯示 HTTP 200、標題 `Example Domain`，並能開啟 `output/` 內的截圖。
6. 說明 `response.status`、`page.title()` 與 role locator 各取得什麼資訊，再進行 AI 介面升級。

## 資料儲存判斷

不需要儲存爬取資料；截圖是本章必要的瀏覽器成果。若要長期監測多個網站，可在 AI 賦能階段選用 SQLite 記錄檢查歷史。

## AI 介面升級

[複製 Prompt 01：使用 tkinter 製作網站健康檢查桌面 App →](../AI介面設計Prompt.md#prompt-01)

[← 返回第 01 章](../../課程章節/第01章_Playwright簡介/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
