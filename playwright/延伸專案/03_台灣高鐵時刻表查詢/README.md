# 台灣高鐵時刻表查詢程式

這是一個使用 Playwright 自動化查詢台灣高鐵時刻表的 Python 程式。

## 功能說明

這個程式會自動：
1. 開啟台灣高鐵官網
2. 處理 Cookie 同意對話框（只需要第一次點擊）
3. 選擇出發站（台北）和到達站（台中）
4. 自動設定出發時間為「現在時間 + 1 小時」
5. 查詢並顯示時刻表資料
6. 顯示票價資訊
7. 列出時刻表下載連結

## 執行前準備

### 1. 安裝 Playwright

```bash
pip install playwright
playwright install chromium
```

### 2. 確認檔案位置

確保你在正確的目錄下執行程式：
```bash
cd playwright/延伸專案/03_台灣高鐵時刻表查詢
```

## 如何執行

在終端機輸入：
```bash
python main.py
```

程式會自動開啟瀏覽器視窗，你可以看到整個查詢過程。

## 程式碼重點說明

### 1. Browser 與 BrowserContext 的差異與優點

在 Playwright 中，`Browser` 與 `BrowserContext` 是兩個非常核心的概念：

| 比較項目 | Browser (瀏覽器實例) | BrowserContext (瀏覽器上下文) |
| :--- | :--- | :--- |
| **定義** | 代表一個實際運行的實體瀏覽器進程 (Chromium, Firefox, WebKit) | 代表瀏覽器內部一個獨立、隔離的隱私會話 (Session) |
| **建立方式** | `p.chromium.launch()` | `browser.new_context()` |
| **資源開銷** | 開銷較大（需要啟動 OS 進程，耗費 CPU 與記憶體） | 開銷極小（建立只需幾毫秒，幾乎不佔用額外資源） |
| **層級關係** | 上層容器，一個 Browser 可管理多個 BrowserContext | 中間層，一個 BrowserContext 可管理多個 Page |
| **隔離程度** | 進程級隔離 | 會話級隔離 (Cookies, LocalStorage, Cache, Viewport 等獨立) |

#### 使用 BrowserContext 的優點

1. **高效能與快速建立**：
   不需要頻繁啟動與關閉實體瀏覽器進程。啟動一次 `Browser` 後，可快速建立與銷毀數百個獨立的 `BrowserContext`，大幅提升爬蟲與測試效率。
2. **多會話獨立隔離 (Multi-session Isolation)**：
   每個 Context 就像一個全新的「無痕視窗」。你可以在同一個瀏覽器實例中，同時登入多個不同帳號或進行平行爬取，彼此的 Cookies 和 Session 絕不衝突。
3. **靈活的狀態保存與注入**：
   如本專案所示，可單獨對 Context 進行 Cookies 的載入 (`context.add_cookies()`) 與匯出 (`context.cookies()`)，輕鬆實現跳過驗證或登入狀態維護。
4. **客製化環境設定**：
   每個 Context 可獨立配置螢幕解析度（如 `viewport={"width": 1280, "height": 720}`）、User Agent、地理位置、時區與權限設定。

### 2. Cookie 處理機制

```python
COOKIES_FILE = "thsrc_cookies.json"
```

程式會將 Cookie 同意記錄保存在 `thsrc_cookies.json` 檔案中，這樣下次執行時就不需要再點擊「我同意」按鈕。

### 3. 自動計算出發時間

```python
now = datetime.now()
departure_time = now + timedelta(hours=1)
```

使用 Python 的 `datetime` 模組，自動計算「現在時間 + 1 小時」作為出發時間。

### 4. 選擇車站

```python
departure_station = page.get_by_label("出發站")
departure_station.select_option("台北")

arrival_station = page.get_by_label("到達站")
arrival_station.select_option("台中")
```

優先使用 Playwright 官方推薦的 `get_by_label()` 方法選擇下拉選單（標籤明確且最具可讀性）。

### 5. 填入日期和時間

```python
date_input = page.get_by_label("出發日期")
date_input.fill(departure_date)

time_input = page.get_by_label("出發時間")
time_input.fill(departure_hour)
```

同樣使用 `get_by_label()` 找到日期與時間輸入欄位，並用 `fill()` 方法填入。

### 6. 等待頁面載入

```python
page.wait_for_load_state("networkidle")
```

等待網路請求完成，確保資料已經載入。

### 7. 抓取資料

```python
train_rows = page.locator("a.tr-row").all()
```

對於頁面上沒有語意化 label/role 的動態資料列表，使用 `locator()` CSS 選擇器找到所有車次列並逐一處理。

## 輸出範例

```
✓ 已載入保存的 cookies
✓ 沒有找到 cookies 對話框，可能已經同意過了
正在等待頁面載入...
✓ 頁面載入完成
✓ 已選擇出發站：台北
✓ 已選擇到達站：台中

✓ 自動設定出發時間為：2025/11/10 15:30
✓ 已填入出發日期：2025/11/10
✓ 已填入出發時間：15:30
✓ 已點擊查詢按鈕
正在等待查詢結果...
✓ 查詢結果已載入

============================================================
時刻表資料
============================================================
出發時間     行車時間     抵達時間     車次      自由座車廂
------------------------------------------------------------
15:35      00:49      16:24      0625     10-12
15:45      00:49      16:34      0627     10-12
...
```

## 常見問題

### Q1: 程式執行時出現「找不到元素」的錯誤？

**A:** 可能是網頁載入速度較慢，可以調整等待時間：
```python
page.locator("#select_location01").wait_for(state="visible", timeout=30000)
```
將 `timeout` 從 15000 改為 30000（30 秒）。

### Q2: 想要查詢其他車站怎麼辦？

**A:** 修改這兩行程式碼：
```python
departure_station.select_option("台北")  # 改成你要的出發站
arrival_station.select_option("台中")    # 改成你要的到達站
```

可用的車站名稱：南港、台北、板橋、桃園、新竹、苗栗、台中、彰化、雲林、嘉義、台南、左營

### Q3: 想要指定特定的日期和時間？

**A:** 直接設定日期和時間字串：
```python
departure_date = "2025/12/25"  # 指定日期
departure_hour = "09:00"       # 指定時間
```

### Q4: 為什麼要用 `headless=False`？

**A:** 這樣可以看到瀏覽器視窗，方便學習和除錯。如果不想看到瀏覽器，可以改成：
```python
browser = p.chromium.launch(headless=True)
```

## 學習重點

這個程式示範了以下 Playwright 技巧：

1. **Browser 與 BrowserContext 概念**：理解實體瀏覽器與獨立上下文（Session）的分離與好處
2. **Cookie 管理**：保存和載入 Cookie
3. **表單操作**：選擇下拉選單、填入文字欄位
4. **等待機制**：等待元素出現、等待網路請求完成
5. **資料抓取**：使用 `locator()` 和 `inner_text()` 抓取資料
6. **JavaScript 執行**：使用 `evaluate()` 執行 JavaScript 程式碼
7. **錯誤處理**：使用 `try-except` 處理可能的錯誤

## 進階練習

1. 修改程式，讓使用者可以輸入出發站、到達站和時間
2. 將查詢結果儲存成 CSV 或 JSON 檔案
3. 加入票價比較功能，找出最便宜的車次
4. 設定定時執行，每天自動查詢特定時段的車次

## 相關資源

- [Playwright 官方文件](https://playwright.dev/python/)
- [台灣高鐵官網](https://www.thsrc.com.tw/)
- [Python datetime 模組說明](https://docs.python.org/zh-tw/3/library/datetime.html)
