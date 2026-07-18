# 理解 PageExpect Navigation 與等待機制

在 Playwright 中，並非所有的 `click` 操作都需要搭配 `expect_navigation` 或其他等待事件。只有當點擊操作會觸發「需要被等待的非同步事件」時，我們才需要使用 context manager (`with` 語法) 來確保程式執行的穩定性。

## 為什麼需要使用 `with`？ (核心觀念)

這是為了避免 **Race Condition (競態條件)**。

如果你分開寫：
```python
page.click("#login-button")
# 如果頁面跳轉非常快，在程式執行到下一行之前，瀏覽器可能已經完成跳轉了...
page.wait_for_url("**/dashboard") # 這裡可能會因為錯過事件而導致 timeout
```

使用 `with` 區塊可以確保「先設定好監聽器，再執行動作」，這樣即使事件發生得再快，Playwright 也能捕捉到。

---

## 什麼時候「一定要用 with」？

當你的操作會觸發以下行為時，必須使用 `with` 來捕捉事件：

### 1. 頁面導航 (Navigation) / 換頁
當點擊會導致 URL 改變或重新載入頁面時。

```python
# 等待新頁面載入完成
with page.expect_navigation():
    page.click("a#next-page")
```

### 2. 發送 API / AJAX 請求
當點擊會觸發背景網路請求，且你需要確認請求完成才能繼續時 (常見於 SPA 單頁應用)。

```python
# 等待特定的 API 回應
with page.expect_response("**/api/user_data"):
    page.click("#load-data-btn")
```

### 3. 開啟新分頁 (New Page / Popup)
當點擊 `target="_blank"` 的連結或按鈕會開啟新視窗時。

```python
# 等待新分頁出現
with context.expect_page() as new_page_info:
    page.click("#open-window-btn")

new_page = new_page_info.value
```

### 4. 檔案下載 (Download)
當點擊會觸發瀏覽器的下載行為時。

```python
# 等待下載事件
with page.expect_download() as download_info:
    page.click("#download-report")
```

---

## 什麼時候「不用 with」？

如果操作只是改變當前頁面的 DOM 狀態，不需要網路導航或特殊事件，通常不需要 `with`。Playwright 的自動等待機制 (Auto-waiting) 已經足夠。

### 1. 純 UI 互動
例如：展開下拉選單、切換頁籤 (Tabs)、顯示/隱藏區塊。

```python
# Playwright 會自動等待元素可點擊
page.click("#dropdown-trigger")
```

### 2. 點擊後等待元素出現
如果點擊後只是要確認某個元素出現，直接使用 `wait_for_selector` 或 `expect` 即可。

```python
page.click("#show-modal")
# 等待 Modal 出現
page.wait_for_selector("#modal-content")
# 或者使用斷言
expect(page.locator("#modal-content")).to_be_visible()
```

---

## 快速判斷準則

請記住這個判斷邏輯：**點擊後，瀏覽器是否會發生「非同步的大動作」？**

*   **會 (換頁、發請求、開新窗)** ➡️ 使用 `with` 包裹。
*   **不會 (只變更畫面樣式)** ➡️ 直接點擊即可。

### 速查表

| 點擊後的行為 | 是否需要 with | 推薦方法 |
| :--- | :---: | :--- |
| **換頁 / 跳轉** | ✅ | `page.expect_navigation()` |
| **發送 API 請求** | ✅ | `page.expect_response()` |
| **開啟新分頁** | ✅ | `context.expect_page()` |
| **下載檔案** | ✅ | `page.expect_download()` |
| **WebSocket 訊息** | ✅ | `page.expect_websocket()` |
| **純畫面變更** | ❌ | 直接 `click()` |
| **展開/收合選單** | ❌ | 直接 `click()` |

---

## 常見錯誤對照

### ❌ 錯誤寫法 (容易卡住或失敗)
```python
page.click("#login")
# 如果登入跳轉太快，這行執行時可能已經跳轉完了，導致永遠等不到導航事件
page.wait_for_navigation()
```

### ✅ 正確寫法 (穩定)
```python
# 先告訴 Playwright：「我預期接下來會有導航事件」
with page.expect_navigation():
    # 然後再執行觸發導航的動作
    page.click("#login")
```

---

## 總結

> **`with` 不是為了「點擊」而存在的，而是為了「捕捉稍縱即逝的事件」而存在的。**