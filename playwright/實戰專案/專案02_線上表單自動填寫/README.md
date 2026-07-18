# 專案 02：線上表單自動填寫

這是[第 02 章：基礎操作](../../課程章節/第02章_基礎操作/README.md)的對應實戰。程式會自動完成 Selenium 官方測試表單，並驗證送出結果。

## 學習重點

- `fill()`、`select_option()`、`check()` 與 `click()`
- 使用 label 與 role 定位表單元素
- 等待 URL 變化與驗證 `Received!`
- 表單送出後的結果驗收

## 執行

```bash
uv run python playwright/實戰專案/專案02_線上表單自動填寫/main.py
```

驗收時確認網址已轉向 `submitted-form.html`，終端顯示 `Received!`。

## AI 介面升級

[複製 Prompt 02：使用 Gradio 製作線上表單助理 →](../AI介面設計Prompt.md#prompt-02)

[← 返回第 02 章](../../課程章節/第02章_基礎操作/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
