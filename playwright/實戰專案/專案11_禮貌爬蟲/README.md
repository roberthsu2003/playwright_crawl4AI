# 專案 11：禮貌爬蟲

這是[第 11 章：反爬蟲對策](../../課程章節/第11章_反爬蟲對策/README.md)的對應實戰。讀取 HTTPBingo robots.txt，並檢查透明 User-Agent、語系、時區、視窗與限速設定。

## 學習重點

- 自訂 User-Agent、locale、timezone 與 viewport
- 讀取 robots.txt 而不自行假設規則
- 主動限制請求速度
- 不繞過 CAPTCHA、不隱藏身分、不高頻請求

## 執行

```bash
uv run python playwright/實戰專案/專案11_禮貌爬蟲/main.py
```

驗收時確認 robots.txt 與 HTTPBingo 收到的 headers 都有正常顯示。

## AI 介面升級

[複製 Prompt 11：使用 Gradio 製作禮貌爬蟲設定助理 →](../AI介面設計Prompt.md#prompt-11)

[← 返回第 11 章](../../課程章節/第11章_反爬蟲對策/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
