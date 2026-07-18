# Crawl4AI 專案：AI 介面與本機儲存 Prompt

先完成各專案的核心爬蟲與驗收，再複製對應 Prompt 給 AI 編程工具。這些 Prompt 會要求 AI 保留 Crawl4AI 核心，並只在資料確實值得保留時加入 CSV、XLSX 或 SQLite。

## 共通限制

- 不使用 Supabase、Firebase、MongoDB Atlas 或其他雲端資料庫。
- 爬蟲函式負責回傳 `list[dict]`，儲存由獨立 repository／export service 處理。
- UI 不得阻塞；錯誤、空資料、執行中與完成狀態都要清楚。
- 不使用假資料代替真實爬取，也不移除速率限制。
- AI 必須更新 README，寫出安裝、啟動、操作、驗收與資料位置。

---

<a id="prompt-01"></a>
## Prompt 01：匯率歷史查詢 App（Streamlit + SQLite）

```text
你是資深 Python 資料應用工程師與 UI/UX 設計師。請閱讀目前專案：
crawl4AI/實戰專案/01_台灣銀行牌告匯率/

先保留並整理既有 Crawl4AI CSS Schema。核心函式只負責擷取並回傳 list[dict]，不可在爬蟲函式中直接寫檔。請新增 Streamlit 繁體中文介面，以及獨立 SQLite repository。

功能需求：
1. 使用者按下「取得最新匯率」才執行一次爬蟲，不建立無限迴圈或背景高頻排程。
2. 頂部顯示更新時間、幣別數、成功/失敗；主表格顯示現金與即期買賣匯率。
3. 提供幣別搜尋、現金/即期切換、買賣價差與匯率趨勢圖。
4. 只有爬取成功且資料通過欄位驗證時，才寫入本機 SQLite。資料表至少包含 captured_at、currency、四種匯率；以 captured_at + currency 避免重複。
5. 提供 CSV 匯出目前篩選結果、刪除指定日期以前資料、清空資料確認對話框。
6. SQLite 放在專案 data/，加入 .gitignore；不得連線任何雲端資料庫。
7. 使用 st.session_state 防止 rerun 重複啟動爬蟲，有 loading、空狀態與可讀錯誤。

請直接建立完整可執行檔案、requirements、資料庫初始化、README 與測試。測試至少涵蓋資料正規化、去重與 CSV 匯出。保留原本 main.py 可獨立執行且不儲存資料。完成後執行語法檢查與不連網的測試，回報啟動方法與驗收結果。
```

<a id="prompt-02"></a>
## Prompt 02：即時股票資訊卡（Gradio，預設不儲存）

```text
你是 Gradio、Crawl4AI 與 UI/UX 專家。請閱讀目前專案：
crawl4AI/實戰專案/02_台灣即時股票資訊/

保留真實動態網頁爬取，將核心重構成接收股票代碼並回傳結構化 dict 的 async 函式，再建立繁體中文 Gradio 介面。

功能需求：
1. 使用 gr.Blocks 與自訂 CSS，提供股票代碼、headless、timeout 與「取得即時資訊」。
2. 以資訊卡顯示名稱、價格、漲跌、開高低、成交量、更新時間，漲跌除了顏色還要有正負號與文字。
3. 顯示爬取步驟、loading、空資料、網站改版可能性與錯誤說明。
4. 不建立資料庫、不自動寫檔、不保存搜尋歷史；資料只存在本次 session。
5. 只有使用者按下「下載本次快照」時，才即時產生一列 CSV，下載後不必保留伺服器歷史檔。
6. 不加入自動高頻刷新，不繞過網站限制。

請產生完整 app.py、核心模組、README、uv 啟動指令與 parser/validation 測試。保留 main.py CLI，完成後執行語法檢查與不連網的核心測試。
```

<a id="prompt-03"></a>
## Prompt 03：批次股票 CSV／XLSX 匯出（tkinter）

```text
你是資深 tkinter 桌面應用與 Python 資料匯出工程師。請閱讀目前專案：
crawl4AI/實戰專案/03_股票批次爬取_GUI/

保留 wantgoo.py 的 Crawl4AI 批次爬蟲與現有 tkinter 搜尋、多選、背景執行緒。請改善介面並新增「使用者主動匯出」功能，不要讓爬取完成時自動寫檔。

功能需求：
1. 結果改為可排序 Treeview，顯示股票代碼、名稱、價格、漲跌、成交量與擷取時間。
2. 只有結果存在時才啟用「匯出 CSV」與「匯出 XLSX」；使用檔案儲存對話框選位置與檔名。
3. CSV 使用 utf-8-sig；XLSX 使用 openpyxl，凍結標題列、加篩選器、合理欄寬與漲跌格式。匯出資料必須等於畫面目前篩選結果。
4. 不建立 SQLite、不使用雲端資料庫、不保存股票搜尋或選取歷史。
5. Crawl4AI 必須在 worker thread 執行，所有 widget 更新安全回到 tkinter 主執行緒。
6. 提供進度、取消、空狀態、錯誤摘要與匯出成功後開啟資料夾功能。

請直接修改成完整可執行專案，更新 requirements、README 與 .gitignore。測試資料正規化、CSV 編碼、XLSX 欄位與「無資料不可匯出」。保留 CLI 模式，完成後執行語法檢查與不連網測試。
```

<a id="prompt-04"></a>
## Prompt 04：即時監控的可選歷史模式（PySide6 + PyQtGraph + SQLite）

```text
你是 PySide6、PyQtGraph、SQLite 與 Crawl4AI 專家。請閱讀目前專案：
crawl4AI/實戰專案/04_股票即時監控_GUI/

請保留即時監控核心，但將 UI 升級為專業桌面看板。預設「歷史模式」關閉；關閉時只更新畫面，不寫任何資料。使用者明確開啟後，才將成功取得的時間序列寫入本機 SQLite。

功能需求：
1. 左側股票搜尋與 watchlist，中間即時表格，右側 PyQtGraph 價格趨勢，下方狀態與日誌。
2. 提供「保存歷史」開關、更新間隔（最低 60 秒）、保留天數與資料庫大小；清楚提示目前是否正在寫入。
3. SQLite 欄位至少包含 captured_at、stock_code、name、price、change、change_percent、volume；建立 stock_code + captured_at 索引並避免重複。
4. 只有成功且通過數值驗證的資料可入庫；N/A 與錯誤結果不可寫入。
5. 可依股票與時間區間查詢、匯出 CSV、刪除過期資料及確認後清空。不得使用雲端資料庫。
6. 使用 QThread/Signal/Slot 或清楚的 worker 邊界，不能凍結 UI，關閉視窗時要停止排程並釋放瀏覽器。
7. 提供深色/淺色主題、非僅顏色的漲跌指示、loading、空狀態與錯誤卡。

請建立模組化完整專案、repository migration、requirements、README 與測試。測試需涵蓋開關關閉時零寫入、去重、錯誤資料不入庫、保留天數清理與 CSV 匯出。完成後執行語法檢查與不連網測試。
```

---

## AI 完成後的學生驗收

- [ ] 我能指出爬蟲核心與儲存模組分別在哪裡。
- [ ] 關閉儲存功能時，爬蟲仍可正常使用。
- [ ] 儲存格式只有 CSV、XLSX 或 SQLite，沒有雲端資料庫。
- [ ] 空資料與失敗結果不會被當成成功資料保存。
- [ ] 我能找到輸出位置、清除資料，並說明每個欄位來源。
- [ ] README 足以讓另一位學生從安裝到驗收完整操作。

[返回 Crawl4AI 實戰專案](README.md)
