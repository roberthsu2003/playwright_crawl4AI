# 專案 06：進階互動巡檢

這是[第 06 章：進階互動](../../課程章節/第06章_進階互動/README.md)的對應實戰。在 The Internet 連續練習懸停、鍵盤、滾動、上傳與下載。

## 學習重點

- `hover()`、`press()` 與 `scroll_into_view_if_needed()`
- `set_input_files()` 上傳檔案
- `expect_download()` 與 `save_as()`
- 將下載成果集中儲存在 `output/`

## 執行

```bash
uv run python playwright/實戰專案/專案06_進階互動巡檢/main.py
```

驗收時確認五個步驟都有結果，上傳檔名正確，且 `output/` 內存在下載檔案。

## AI 介面升級

[複製 Prompt 06：使用 PySide6 + PyQtGraph 製作互動巡檢工具 →](../AI介面設計Prompt.md#prompt-06)

[← 返回第 06 章](../../課程章節/第06章_進階互動/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
