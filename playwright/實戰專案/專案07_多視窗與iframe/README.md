# 專案 07：多視窗與 iframe

這是[第 07 章：多頁面與框架處理](../../課程章節/第07章_多頁面與框架處理/README.md)的對應實戰。程式會處理新分頁、JavaScript alert 與 iframe 內容。

## 學習重點

- `expect_popup()` 等待新視窗
- 監聽與回應 JavaScript dialog
- `frame_locator()` 進入 iframe
- 正確關閉 popup、context 與 browser

## 完成步驟

1. 手動開啟 The Internet 的 Windows、JavaScript Alerts 與 iframe 頁面。
2. 開啟 [`main.py`](main.py)，分別找出 popup、dialog 與 frame locator 三段。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案07_多視窗與iframe/main.py
```

4. 觀察 popup 為另一個 Page，而 iframe 仍在原頁面的 frame 中。
5. 驗收顯示 `New Window`、alert 成功訊息與 iframe 內文字。
6. 將 alert 改成 confirm 或 prompt 練習後還原，再使用 AI Prompt 建立互動實驗室。

## 資料儲存判斷

不需要。三項結果只用來驗證瀏覽器互動，AI 介面保留本次 session 狀態即可。

## AI 介面升級

[複製 Prompt 07：使用 Flask 製作瀏覽器互動實驗室 →](../AI介面設計Prompt.md#prompt-07)

[← 返回第 07 章](../../課程章節/第07章_多頁面與框架處理/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
