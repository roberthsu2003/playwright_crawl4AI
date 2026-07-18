# 專案 08：網頁存證報告

這是[第 08 章：截圖與錄影](../../課程章節/第08章_截圖與錄影/README.md)的對應實戰。將 Wikipedia 頁面製作成整頁截圖、元素截圖、區域截圖、錄影與 PDF。

## 學習重點

- 整頁、元素與 clip 區域截圖
- 使用 Chromium 產生 PDF
- browser context 錄影與正確關閉時機
- 建立統一的成果資料夾

## 執行

```bash
uv run python playwright/實戰專案/專案08_網頁存證報告/main.py
```

驗收時檢查 `output/` 內的 PNG、PDF 與 `video/` 錄影，確認檔案都能開啟。

## AI 介面升級

[複製 Prompt 08：使用 Streamlit 製作網頁存證作品庫 →](../AI介面設計Prompt.md#prompt-08)

[← 返回第 08 章](../../課程章節/第08章_截圖與錄影/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
