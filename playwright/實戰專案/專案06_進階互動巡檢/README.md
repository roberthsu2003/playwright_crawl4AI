# 專案 06：進階互動巡檢

這是[第 06 章：進階互動](../../課程章節/第06章_進階互動/README.md)的對應實戰。在 The Internet 連續練習懸停、鍵盤、滾動、上傳與下載。

## 學習重點

- `hover()`、`press()` 與 `scroll_into_view_if_needed()`
- `set_input_files()` 上傳檔案
- `expect_download()` 與 `save_as()`
- 將下載成果集中儲存在 `output/`

## 完成步驟

1. 手動操作 The Internet 的 Hovers、Key Presses、Large & Deep DOM、Upload 與 Download 頁面。
2. 開啟 [`main.py`](main.py)，將五段操作對應到五個 Playwright API。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案06_進階互動巡檢/main.py
```

4. 逐行檢查終端結果；下載步驟會把網站提供的檔案放入 `output/`。
5. 驗收五個步驟都有結果、上傳檔名正確，且下載檔可以開啟。
6. 任選一個步驟說明「動作、等待、驗證」三部分，再進行 AI 介面升級。

## 資料儲存判斷

不需要儲存爬取資料。`student_upload.txt` 與下載檔是上傳／下載章節的必要操作產物，不是資料分析結果。

## AI 介面升級

[複製 Prompt 06：使用 PySide6 + PyQtGraph 製作互動巡檢工具 →](../AI介面設計Prompt.md#prompt-06)

[← 返回第 06 章](../../課程章節/第06章_進階互動/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
