# 專案 10：登入狀態保存

這是[第 10 章：登入與 Cookie 處理](../../課程章節/第10章_登入與Cookie處理/README.md)的對應實戰。登入 SauceDemo 後儲存 storage state，再用新 browser context 驗證狀態可重複使用。

## 學習重點

- 自動登入與登入後 URL 驗證
- Cookie、localStorage 與 storage state
- `storage_state()` 儲存成 `auth.json`
- 在新 context 載入既有狀態

## 完成步驟

1. 先了解 `storage state` 包含 Cookie 與 localStorage，可能具有登入權限。
2. 開啟 [`main.py`](main.py)，找出第一次登入、寫出狀態、第二個 context 載入狀態三段。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案10_登入狀態保存/main.py
```

4. 確認第二個 context 沒有再次輸入密碼，仍能進入 inventory。
5. 驗收 `output/auth.json` 已建立；完成後刪除測試狀態，且不可分享或提交到 Git。
6. 能說明狀態檔的用途與風險後，再使用 AI Prompt 建立安全管理器。

## 資料儲存判斷

`auth.json` 是本章必須練習的瀏覽器狀態，不是爬取資料。不要再轉存 CSV、XLSX 或 SQLite；AI 介面也不得顯示 Cookie value 或保存密碼。

## AI 介面升級

[複製 Prompt 10：使用 PySide6 製作登入狀態管理器 →](../AI介面設計Prompt.md#prompt-10)

[← 返回第 10 章](../../課程章節/第10章_登入與Cookie處理/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
