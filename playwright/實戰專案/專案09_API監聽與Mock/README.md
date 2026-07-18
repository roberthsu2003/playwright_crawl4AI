# 專案 09：API 監聽與 Mock

這是[第 09 章：網路請求與回應](../../課程章節/第09章_網路請求與回應/README.md)的對應實戰。監聽 JSONPlaceholder 真實 API，再以 Playwright route 提供 Mock JSON 回應。

## 學習重點

- request/response event
- `expect_response()` 等待指定 API
- `page.route()` 與 `route.fulfill()`
- 比較真實與 Mock 回應

## 完成步驟

1. 用瀏覽器查看 JSONPlaceholder 的 `/posts/1`，理解真實 JSON 格式。
2. 開啟 [`main.py`](main.py)，對照 request event、`expect_response()` 與 `route.fulfill()`。
3. 在 repo 根目錄完成共用安裝後執行：

```bash
uv run python playwright/實戰專案/專案09_API監聽與Mock/main.py
```

4. 比較真實回應與 Mock 回應，確認第二次請求確實被 route 攔截。
5. 驗收先收到 HTTP 200 真實標題，再收到「教室 Mock 資料」。
6. 嘗試將 Mock status 改為 404 後還原，再進行 AI API 平台升級。

## 資料儲存判斷

核心練習不需要儲存。AI 平台若要支援「最近執行紀錄」，可用 SQLite 保留 request/response 摘要；限制筆數並提供清除功能，不使用雲端資料庫。

## AI 介面升級

[複製 Prompt 09：使用 FastAPI 製作 API 監聽與 Mock 平台 →](../AI介面設計Prompt.md#prompt-09)

[← 返回第 09 章](../../課程章節/第09章_網路請求與回應/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
