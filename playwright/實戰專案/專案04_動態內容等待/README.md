# 專案 04：動態內容等待

這是[第 04 章：等待與同步](../../課程章節/第04章_等待與同步/README.md)的對應實戰。在 The Internet 啟動延遲內容，正確等待 `Hello World!` 出現。

## 學習重點

- Playwright 自動等待
- `wait_for(state="visible")`
- Web-first assertion 的自動重試
- 驗證 loading 消失，不以固定 sleep 猜測時間

## 完成步驟

1. 手動開啟 Dynamic Loading 頁面，按下 Start，觀察 loading 與結果出現的順序。
2. 開啟 [`main.py`](main.py)，找出自動等待、`wait_for()` 與 `expect()`。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案04_動態內容等待/main.py
```

4. 將 timeout 暫時改短，觀察 timeout 錯誤後還原；不要改成固定 `sleep`。
5. 驗收終端顯示 `Hello World!` 與「載入提示已消失」。
6. 能說明三種等待方式後，再使用 AI Prompt 製作可比較 timeout 的實驗介面。

## 資料儲存判斷

核心課程不需要儲存。AI 實驗室可選擇匯出 CSV，比較不同 timeout 與等待策略的耗時；不需要 SQLite。

## AI 介面升級

[複製 Prompt 04：使用 Streamlit 製作動態等待實驗室 →](../AI介面設計Prompt.md#prompt-04)

[← 返回第 04 章](../../課程章節/第04章_等待與同步/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
