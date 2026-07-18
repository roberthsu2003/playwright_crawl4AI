# 專案 04：動態內容等待

這是[第 04 章：等待與同步](../../課程章節/第04章_等待與同步/README.md)的對應實戰。在 The Internet 啟動延遲內容，正確等待 `Hello World!` 出現。

## 學習重點

- Playwright 自動等待
- `wait_for(state="visible")`
- Web-first assertion 的自動重試
- 驗證 loading 消失，不以固定 sleep 猜測時間

## 執行

```bash
uv run python playwright/實戰專案/專案04_動態內容等待/main.py
```

驗收時確認終端顯示 `Hello World!` 與「載入提示已消失」。

## AI 介面升級

[複製 Prompt 04：使用 Streamlit 製作動態等待實驗室 →](../AI介面設計Prompt.md#prompt-04)

[← 返回第 04 章](../../課程章節/第04章_等待與同步/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
