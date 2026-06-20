# Webwright 的使用方式

Webwright 是整合在 Claude Code 中的 Playwright 瀏覽器自動化工具，能以「程式即動作（code-as-action）」的方式執行網頁任務，並將截圖與操作紀錄自動儲存至 `final_runs/run_<id>/` 資料夾。

---

## 兩種使用模式

### 1. `/webwright` — 一次性網頁任務

適合**直接完成**某個網頁操作，例如填表、搜尋、資料擷取。

**使用方式**：在 Claude Code 對話中直接描述任務：

* **簡單範例（資料查詢）**：
  ```
  /webwright 前往臺灣銀行牌告匯率官網，查詢並回報最新的美金現鈔買入與賣出匯率
  ```

* **複雜範例（多步驟操作）**：
  ```
  /webwright 前往 Google Flights，搜尋 8/15 從西雅圖飛往紐約的最低票價
  ```

Claude 會：
1. 啟動本機 Playwright Chromium 瀏覽器
2. 逐步執行操作（導航 → 填表 → 點擊 → 擷取資料）
3. 在每個關鍵步驟截圖
4. 將結果（截圖 + 操作記錄）儲存至 `final_runs/run_<id>/`
5. 視覺化驗證結果是否正確

---

### 2. `/webwright:craft` — 製作可重複使用的腳本

適合**參數化**網頁任務，製成可多次執行的腳本工具。

**使用方式**：

```
/webwright:craft 製作一個可輸入出發地、目的地、日期的機票搜尋腳本
```

Claude 會將任務封裝成帶參數的腳本，方便日後以不同輸入值反覆執行。

---

## 輸出結構

每次執行後，結果儲存在 `final_runs/run_<數字>/`：

```
final_runs/
└── run_5/
    ├── 01_initial.png          # 初始頁面截圖
    ├── 02_after_origin.png     # 填入出發地後截圖
    ├── 03_after_dest.png       # 填入目的地後截圖
    ├── 04_cal_open.png         # 開啟日曆後截圖
    ├── 05_dates_sel.png        # 選好日期後截圖
    ├── 06_results.png          # 搜尋結果截圖
    ├── 07_final.png            # 最終確認截圖
    └── final_script_log.txt    # 完整操作紀錄
```

### `final_script_log.txt` 範例

```
[15:25:51] CP1: 導航 Google Flights
[15:25:52] CP2: 出發地 Seattle
[15:25:56]   → 選擇 (Seattle): Seattle, Washington, USA
[15:25:57] CP3: 目的地 JFK
[15:26:03] CP4: 點擊 Departure
[15:26:05] CP5: 點擊 Aug 15
[15:26:05] CP6: 點擊 Aug 20
[15:26:05] CP7: 點擊 Done
[15:26:05] CP8: 搜尋
[15:26:20] CP9: 最低票價: $2,029
[15:26:20] CP10: 完成
```

---

## 適用情境

| 情境 | 建議指令 |
|------|---------|
| 擷取網頁資料（一次性） | `/webwright` |
| 自動填表並送出 | `/webwright` |
| 製作可重複執行的爬蟲腳本 | `/webwright:craft` |
| 多頁面流程自動化 | `/webwright` |
| 需要截圖作為執行證明 | `/webwright` |

---

## 與 Playwright / Crawl4AI 的差異

| 比較項目 | Webwright | Playwright（直接撰寫） | Crawl4AI |
|---------|-----------|----------------------|---------|
| 使用方式 | 自然語言描述任務 | 手動撰寫 Python 腳本 | 高階 API + LLM 解析 |
| 適合對象 | 快速驗證、一次性任務 | 需精確控制的場景 | 大規模、結構化資料擷取 |
| 輸出 | 截圖 + 操作紀錄 | 自訂 | Markdown / JSON |
| 學習曲線 | 最低 | 中等 | 低（框架封裝） |

---

## 注意事項

1. **建議安裝 Chrome 與 Firefox**：執行 `playwright install chrome firefox`
2. **需啟動虛擬環境**：執行前先 `source .venv/bin/activate`
3. **執行記錄自動累積**：每次執行會新增 `run_N` 資料夾，不會覆蓋舊結果
4. **截圖為視覺驗證依據**：Claude 會透過截圖確認每個步驟是否成功

---

## 快速開始範例

```
# 範例 1：擷取台灣銀行今日匯率
/webwright 前往台灣銀行牌告匯率頁面，擷取今日美元兌台幣的買入與賣出價

# 範例 2：搜尋 PTT 最新文章標題
/webwright 前往 PTT 八卦版，列出首頁前 10 篇文章的標題與推文數

# 範例 3：檢查網站是否正常運作並截圖存證
/webwright 前往 https://example.com 並截圖確認頁面正常顯示

# 範例 4：建立可重複使用的商品價格擷取腳本
/webwright:craft 製作一個可輸入商品網址的價格擷取腳本，輸出商品名稱、目前價格與擷取時間

# 範例 5：建立網站狀態監控腳本
/webwright:craft 製作一個可輸入網址的網站監控腳本，檢查 HTTP 狀態、頁面標題與指定文字是否存在，並儲存截圖

# 範例 6：建立自動填寫表單腳本
/webwright:craft 製作一個可輸入姓名、電子郵件與留言內容的表單填寫腳本，送出前先截圖並等待使用者確認

# 範例 7：建立分頁資料擷取腳本
/webwright:craft 製作一個可輸入列表頁網址與最大頁數的爬蟲腳本，自動翻頁並將標題、連結與日期輸出為 JSON
```
