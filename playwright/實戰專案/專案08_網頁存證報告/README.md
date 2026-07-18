# 專案 08：網頁存證報告

這是[第 08 章：截圖與錄影](../../課程章節/第08章_截圖與錄影/README.md)的對應實戰。將 Wikipedia 頁面製作成整頁截圖、元素截圖、區域截圖、錄影與 PDF。

## 學習重點

- 整頁、元素與 clip 區域截圖
- 使用 Chromium 產生 PDF
- browser context 錄影與正確關閉時機
- 建立統一的成果資料夾

## 完成步驟

1. 開啟 [`main.py`](main.py)，確認目標 URL、viewport 與 `output/` 路徑。
2. 依序找出整頁、元素、clip 截圖、PDF 與錄影設定。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案08_網頁存證報告/main.py
```

4. 等程式正常關閉 page 與 context；錄影要到關閉後才會完整寫入。
5. 驗收 `output/` 內三張 PNG、PDF 與 `video/` 錄影都能開啟。
6. 更換一個公開頁面測試後，再使用 AI Prompt 建立作品庫。

## 資料儲存判斷

PNG、PDF、影片就是本章的必要成果，因此由核心程式直接保存。AI 作品庫可選用 SQLite 只記錄檔名、來源網址、建立時間與大小；實體檔仍保留在本機資料夾。

## AI 介面升級

[複製 Prompt 08：使用 Streamlit 製作網頁存證作品庫 →](../AI介面設計Prompt.md#prompt-08)

[← 返回第 08 章](../../課程章節/第08章_截圖與錄影/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
