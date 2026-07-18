# 專案 07：多視窗與 iframe

這是[第 07 章：多頁面與框架處理](../../課程章節/第07章_多頁面與框架處理/README.md)的對應實戰。程式會處理新分頁、JavaScript alert 與 iframe 內容。

## 學習重點

- `expect_popup()` 等待新視窗
- 監聽與回應 JavaScript dialog
- `frame_locator()` 進入 iframe
- 正確關閉 popup、context 與 browser

## 執行

```bash
uv run python playwright/實戰專案/專案07_多視窗與iframe/main.py
```

驗收時確認顯示 `New Window`、alert 成功訊息與 iframe 內的文字。

## AI 介面升級

[複製 Prompt 07：使用 Flask 製作瀏覽器互動實驗室 →](../AI介面設計Prompt.md#prompt-07)

[← 返回第 07 章](../../課程章節/第07章_多頁面與框架處理/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
