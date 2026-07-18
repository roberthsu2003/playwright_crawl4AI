# 專案 09：API 監聽與 Mock

這是[第 09 章：網路請求與回應](../../課程章節/第09章_網路請求與回應/README.md)的對應實戰。監聽 JSONPlaceholder 真實 API，再以 Playwright route 提供 Mock JSON 回應。

## 學習重點

- request/response event
- `expect_response()` 等待指定 API
- `page.route()` 與 `route.fulfill()`
- 比較真實與 Mock 回應

## 執行

```bash
uv run python playwright/實戰專案/專案09_API監聽與Mock/main.py
```

驗收時確認先收到 HTTP 200 真實標題，再收到「教室 Mock 資料」。

## AI 介面升級

[複製 Prompt 09：使用 FastAPI 製作 API 監聽與 Mock 平台 →](../AI介面設計Prompt.md#prompt-09)

[← 返回第 09 章](../../課程章節/第09章_網路請求與回應/README.md) | [返回實戰專案總覽](../README.md) | [主程式](main.py)
