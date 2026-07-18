# 專案 03：購物網站元素定位

這是[第 03 章：元素定位](../../課程章節/第03章_元素定位/README.md)的對應實戰。在 SauceDemo 登入後，使用多種穩定定位方式選取商品並加入購物車。

## 學習重點

- placeholder、role、test id、CSS 與 `filter()`
- 將 `data-test` 設為 Playwright test id
- 在特定商品卡片範圍內定位
- Web-first assertion 驗證 URL 與購物車數量

## 完成步驟

1. 手動登入 SauceDemo，找到 Backpack 商品卡與購物車圖示。
2. 開啟 [`main.py`](main.py)，對照 placeholder、role、test id、CSS 與 `filter()` 五種定位方式。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案03_購物網站元素定位/main.py
```

4. 確認程式先縮小到指定商品卡，再於卡片內找按鈕，避免點錯商品。
5. 驗收終端顯示 `Sauce Labs Backpack`，購物車數量為 1。
6. 改定位另一項商品測試；完成後再交由 AI 建立控制台。專案僅操作公開測試站，不包含真實付款。

## 資料儲存判斷

不需要。商品與購物車只是元素定位練習，不建立商品資料庫，也不保存登入資訊。

## AI 介面升級

[複製 Prompt 03：使用 Flask 製作購物自動化控制台 →](../AI介面設計Prompt.md#prompt-03)

[← 返回第 03 章](../../課程章節/第03章_元素定位/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
