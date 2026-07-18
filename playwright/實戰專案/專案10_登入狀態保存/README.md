# 專案 10：登入狀態保存

這是[第 10 章：登入與 Cookie 處理](../../課程章節/第10章_登入與Cookie處理/README.md)的對應實戰。登入 SauceDemo 後儲存 storage state，再用新 browser context 驗證狀態可重複使用。

## 學習重點

- 自動登入與登入後 URL 驗證
- Cookie、localStorage 與 storage state
- `storage_state()` 儲存成 `auth.json`
- 在新 context 載入既有狀態

## 執行

```bash
uv run python playwright/實戰專案/專案10_登入狀態保存/main.py
```

驗收時確認 `output/auth.json` 已建立，第二個 context 未再輸入密碼便進入 inventory。`auth.json` 含敏感狀態，不可分享或提交到 Git。

## AI 介面升級

[複製 Prompt 10：使用 PySide6 製作登入狀態管理器 →](../AI介面設計Prompt.md#prompt-10)

[← 返回第 10 章](../../課程章節/第10章_登入與Cookie處理/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
