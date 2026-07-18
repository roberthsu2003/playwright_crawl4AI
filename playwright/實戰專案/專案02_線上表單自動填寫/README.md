# 專案 02：線上表單自動填寫

這是[第 02 章：基礎操作](../../課程章節/第02章_基礎操作/README.md)的對應實戰。程式會自動完成 Selenium 官方測試表單，並驗證送出結果。

## 學習重點

- `fill()`、`select_option()`、`check()` 與 `click()`
- 使用 label 與 role 定位表單元素
- 等待 URL 變化與驗證 `Received!`
- 表單送出後的結果驗收

## 完成步驟

1. 用瀏覽器手動開啟 Selenium Web Form，觀察欄位標籤與送出後網址。
2. 開啟 [`main.py`](main.py)，依序找出 `fill()`、`select_option()`、`check()` 與 `click()`。
3. 在 repo 根目錄完成 `uv sync` 與 `uv run playwright install chromium`，再執行：

```bash
uv run python playwright/實戰專案/專案02_線上表單自動填寫/main.py
```

4. 觀察程式如何等待網址改變，以及如何等待 `Received!` 可見。
5. 確認終端網址包含 `submitted-form.html`，並顯示 `Received!`。
6. 更換一個輸入值重新驗證，成功後再使用 AI Prompt 建立介面。

## 資料儲存判斷

不需要。這個專案的重點是操作與驗證表單，不應保存練習密碼或表單內容；AI 介面只顯示本次結果與截圖。

## AI 介面升級

[複製 Prompt 02：使用 Gradio 製作線上表單助理 →](../AI介面設計Prompt.md#prompt-02)

[← 返回第 02 章](../../課程章節/第02章_基礎操作/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
