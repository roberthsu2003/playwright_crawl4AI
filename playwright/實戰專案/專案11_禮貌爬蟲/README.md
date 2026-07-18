# 專案 11：禮貌爬蟲

這是[第 11 章：反爬蟲對策](../../課程章節/第11章_反爬蟲對策/README.md)的對應實戰。讀取 HTTPBingo robots.txt，並檢查透明 User-Agent、語系、時區、視窗與限速設定。

## 學習重點

- 自訂 User-Agent、locale、timezone 與 viewport
- 讀取 robots.txt 而不自行假設規則
- 主動限制請求速度
- 不繞過 CAPTCHA、不隱藏身分、不高頻請求

## 完成步驟

1. 先閱讀目標站 robots.txt，確認它是規範提示而非用來猜測繞過方法。
2. 開啟 [`main.py`](main.py)，檢查透明 User-Agent、語系、時區、viewport 與請求間隔。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案11_禮貌爬蟲/main.py
```

4. 比較程式設定與 HTTPBingo 實際收到的 headers。
5. 驗收 robots.txt、User-Agent、Accept-Language 與 viewport 都正常顯示。
6. 修改 bot 名稱與間隔練習後還原，再使用 AI Prompt 建立設定助理。

## 資料儲存判斷

不需要。這是規範與設定檢查；AI 介面最多提供本次 JSON/CSV 報告下載，不建立歷史資料庫。

## AI 介面升級

[複製 Prompt 11：使用 Gradio 製作禮貌爬蟲設定助理 →](../AI介面設計Prompt.md#prompt-11)

[← 返回第 11 章](../../課程章節/第11章_反爬蟲對策/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
