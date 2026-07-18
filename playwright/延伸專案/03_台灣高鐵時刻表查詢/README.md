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

### 1. Cookie 處理機制

```python
COOKIES_FILE = "thsrc_cookies.json"
```

程式會將 Cookie 同意記錄保存在 `thsrc_cookies.json` 檔案中，這樣下次執行時就不需要再點擊「我同意」按鈕。

### 2. 自動計算出發時間

```python
now = datetime.now()
departure_time = now + timedelta(hours=1)
```

使用 Python 的 `datetime` 模組，自動計算「現在時間 + 1 小時」作為出發時間。

### 3. 選擇車站

```python
departure_station.select_option("台北")
arrival_station.select_option("台中")
```

使用 `select_option()` 方法選擇下拉選單中的選項。

### 4. 填入日期和時間

```python
date_input.fill(departure_date)
time_input.fill(departure_hour)
```

使用 `fill()` 方法填入表單欄位。

### 5. 等待頁面載入

```python
page.wait_for_load_state("networkidle")
```

等待網路請求完成，確保資料已經載入。

### 6. 抓取資料

```python
train_rows = page.locator("a.tr-row").all()
```

使用 `locator()` 找到所有車次資料，然後用迴圈逐一處理。

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

1. **Cookie 管理**：保存和載入 Cookie
2. **表單操作**：選擇下拉選單、填入文字欄位
3. **等待機制**：等待元素出現、等待網路請求完成
4. **資料抓取**：使用 `locator()` 和 `inner_text()` 抓取資料
5. **JavaScript 執行**：使用 `evaluate()` 執行 JavaScript 程式碼
6. **錯誤處理**：使用 `try-except` 處理可能的錯誤

## 進階練習

1. 修改程式，讓使用者可以輸入出發站、到達站和時間
2. 將查詢結果儲存成 CSV 或 JSON 檔案
3. 加入票價比較功能，找出最便宜的車次
4. 設定定時執行，每天自動查詢特定時段的車次

## 相關資源

- [Playwright 官方文件](https://playwright.dev/python/)
- [台灣高鐵官網](https://www.thsrc.com.tw/)
- [Python datetime 模組說明](https://docs.python.org/zh-tw/3/library/datetime.html)
