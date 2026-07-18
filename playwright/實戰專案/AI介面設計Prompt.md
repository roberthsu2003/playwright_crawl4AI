# AI 介面設計 Prompt 手冊

完成 Playwright 核心功能後，可以把原本只在終端機顯示的結果，升級成桌面應用程式、資料儀表板、互動網站或 Web API。

下面的 12 份 Prompt 都是完整任務說明。學生只要在 AI 編程工具中開啟本專案，再複製對應 Prompt，就可以請 AI 直接建立介面。

> AI 產生介面之後，學生仍需自己執行、檢查錯誤訊息、驗收輸出檔，並能說明 UI 如何呼叫 Playwright 核心函式。

## 介面工具怎麼選？

| 工具 | 類型 | 最適合 | 優點 | 需注意 |
|---|---|---|---|---|
| `tkinter` | 桌面應用 | Python 初學者、表單、單機工具 | Python 內建，無需額外框架 | 預設樣式較傳統，需自訂 theme |
| `PySide6` / `PySide5` | 專業桌面應用 | 多視窗、系統工具、大型 GUI | 佈局與元件完整，可打包成 App | 學習曲線比 tkinter 高 |
| `PyQtGraph` | 桌面圖表 | 即時速度、請求量、效能監控 | 即時繪圖速度快 | 通常要搭配 PySide/PyQt |
| `Gradio` | 快速 Web UI | AI Demo、輸入→執行→輸出的工具 | 程式少、容易分享 | 複雜網站的自由度較低 |
| `Streamlit` | 資料 Web App | 報告、圖片、CSV、資料探索 | 很適合 Python 資料產品 | 每次互動可能重跑程式，要管理 state |
| `Dash` | 分析儀表板 | KPI、圖表、篩選、效能比較 | Plotly 圖表整合強 | callback 的概念需要練習 |
| `Flask` | 自訂 Web 網站 | 有品牌感的網頁、多頁流程 | HTML/CSS/JS 自由度高 | 需自行處理前後端結構 |
| `FastAPI` | Web API | 將爬蟲能力提供給其他系統 | 型別驗證、async、Swagger 文件 | 它是 API 後端，不是完整前端 |

### 版本建議

新專案建議使用 `PySide6`，因為它是 Qt 目前持續維護的官方 Python binding。若學校環境已統一使用 `PySide5`，可要求 AI 將 import 與少數 API 調整為 PySide5。

## 共同的介面品質標準

每份 Prompt 都已包含以下原則：

- 保留原本 Playwright 核心邏輯，先拆成可重複使用的函式，再接 UI。
- 長時間任務不能阻塞畫面，並要有進度、執行狀態、錯誤訊息與取消機制。
- 介面使用繁體中文，有明確層級、一致間距、無障礙對比與響應式佈局。
- 不把密碼、Cookie 或 token 寫死在程式碼。
- 不用假資料假裝功能完成；空狀態、載入、成功、失敗都要能看見。
- 資料儲存只在各 Prompt 明確要求時加入，且只能使用 CSV、XLSX 或 SQLite；不得使用 Firebase、Supabase 或其他雲端資料庫。
- 不值得保留的操作型資料只顯示在當次介面，不為了展示技術而建立資料庫。
- 產生完整可執行程式、套件說明、執行指令、README 與基本測試。

---

<a id="prompt-01"></a>
## Prompt 01：網站健康檢查桌面 App（tkinter）

適合讓學生第一次把 Python 終端程式改成桌面應用。

```text
你是資深 Python 桌面應用工程師與 UI/UX 設計師。請直接為目前專案建立一個繁體中文 tkinter 網站健康檢查 App。

現有核心程式：playwright/實戰專案/專案01_網站健康檢查/main.py

請先閱讀現有程式，將「開啟瀏覽器、導航、取得 HTTP 狀態、頁面標題、主標題、儲存截圖」重構為可供 UI 呼叫的函式，不要改變原本可執行行為。

介面需求：
1. 1200x760 左右雙欄佈局，深藍與青綠色系，使用 ttk.Style 製作現代化卡片、按鈕與狀態標籤。
2. 左側有 URL、瀏覽器（Chromium/Firefox/WebKit）、headless 開關、timeout 輸入與「開始檢查」按鈕。
3. 右側顯示 HTTP 狀態、回應時間、頁面標題、最終 URL、成功/警告/失敗狀態與截圖預覽。
4. 底部有可滾動的執行日誌、「開啟輸出資料夾」與「清除結果」。
5. Playwright 必須放在 background worker thread，絕對不能卡住 tkinter mainloop；所有 UI 更新必須安全回到主執行緒。
6. 驗證 URL 與 timeout，錯誤時顯示對學生有幫助的訊息，不只顯示 traceback。
7. 保留原本 CLI 執行方式，新增 gui.py 做為 UI 入口。
8. 本專案預設不建立資料庫；若實作歷史監測功能，只能選用 SQLite，並提供清除紀錄功能。

請直接建立完整檔案，不要只給範例片段或偽程式碼。同時更新 requirements.txt 與 README，提供 uv 安裝/執行指令，並加入對核心函式的基本測試。完成後請實際執行語法檢查與 smoke test，回報修改檔案、執行方法與驗收結果。
```

<a id="prompt-02"></a>
## Prompt 02：線上表單助理（Gradio）

```text
你是擅長 Gradio 與 Playwright 的 Python 全端工程師。請為目前專案建立繁體中文、精緻、可教學的「線上表單自動化助理」。

現有核心程式：playwright/實戰專案/專案02_線上表單自動填寫/main.py

必須保留 Selenium Web Form 的真實 Playwright 操作，先將自動填寫邏輯重構成可傳入姓名、密碼練習值、說明、下拉選項、checkbox 與 radio 的函式，再由 Gradio UI 呼叫。

介面需求：
1. 使用 gr.Blocks 與自訂 CSS，畫面有頂部品牌標題、步驟指示、左側表單、右側執行結果。
2. 表單含姓名、練習用密碼、備註、選項、checkbox、radio、headless 開關與 timeout。密碼欄預設隱藏，不寫入 log。
3. 按下執行後顯示 loading、目前步驟、最終 URL、Received! 驗證結果、總耗時與成功/失敗摘要。
4. 成功與失敗時都儲存截圖，並在 UI 顯示預覽與下載連結。
5. 加入「載入示範資料」、「清除」與「執行」按鈕，並防止重複點擊產生多個瀏覽器。
6. 不要讓 UI 與 Playwright 細節綁死；核心層回傳結構化 dict，UI 只負責顯示。
7. 不保存表單輸入、練習密碼或執行歷史；只保留本次 session 與成功／失敗截圖。

請建立 app.py、必要的核心模組與 README，不要使用偽程式碼。列出 uv 安裝與執行指令，加入輸入驗證、例外處理與基本測試。完成後實際做 smoke test，並確認原本 main.py 仍可獨立執行。
```

<a id="prompt-03"></a>
## Prompt 03：購物自動化控制台（Flask）

```text
你是資深 Flask 全端工程師、UI/UX 設計師與 Playwright 自動化專家。請為以下專案建立一個「電商自動化控制台」：
playwright/實戰專案/專案03_購物網站元素定位/main.py

先讀懂現有 SauceDemo 登入、商品定位與加入購物車流程，將它拆成 login、list_products、add_to_cart、get_cart_summary 等可測試函式。不要改成抓假資料，也不要把帳號密碼寫死在前端。

網站介面需求：
1. 使用 Flask + Jinja2 + 原生 CSS/JavaScript，建立具有電商品牌感的響應式介面；不依賴大型前端框架。
2. 頂部有品牌、執行狀態、購物車 badge；主區顯示商品卡片網格，含名稱、價格、定位策略標籤與加入按鈕。
3. 左側篩選器可設定價格上限、商品關鍵字、排序、headless與 timeout。
4. 右側抽屜顯示購物車清單、總價、執行步驟、截圖與「重新開始」。
5. 使用 fetch 或 SSE 更新任務狀態，長時間 Playwright 任務不得阻塞 Flask request。先做適合單人本機教學的輕量 task manager，不要過度工程化。
6. 有 skeleton loading、空狀態、toast、可讀的錯誤卡、鍵盤 focus 樣式與行動裝置佈局。
7. 明確說明這是公開測試站，不實作付款，不把流程套用到真實商店。
8. 不建立商品或購物車資料庫，不保存帳密；資料只存在本次使用者 session。

請直接產生完整可執行的檔案結構、templates、static、Python 模組、requirements 與 README。保留 CLI，加入核心層測試與 Flask route 測試，並實際執行 smoke test。
```

<a id="prompt-04"></a>
## Prompt 04：動態等待實驗室（Streamlit）

```text
你是 Streamlit 資料應用工程師與 Playwright 教學專家。請為以下專案建立一個繁體中文「Playwright 等待策略實驗室」：
playwright/實戰專案/專案04_動態內容等待/main.py

先將現有 The Internet dynamic loading 邏輯重構為可傳入 timeout 與等待策略的核心函式，回傳每一階段的時間、最終文字、成功與否、錯誤類型、截圖路徑。

介面要求：
1. 寬螢幕三區塊：左側實驗參數、中央流程時間線、右側結果與觀察。
2. 可選「自動等待」、「wait_for visible」、「Web-first assertion」與「故意使用過短 timeout」，但不要建議使用固定 sleep。
3. 用 KPI 卡顯示總耗時、等待時間、結果文字與狀態；用 Plotly 時間線顯示 goto、click、loading、visible、assertion。
4. 成功顯示綠色「Hello World!」；失敗顯示可讀的 timeout 說明、失敗截圖與「如何修正」教學卡。
5. 使用 st.session_state 保留最近 10 次結果，可比較不同 timeout，並下載 CSV。
6. 需有執行中狀態、重複執行防護、空狀態、錯誤處理與說明工具提示。
7. 最近 10 次結果只放在 session_state；只有使用者按下下載時才產生 CSV，不建立資料庫。

請建立完整 app.py、核心模組、requirements 與 README，保留 main.py CLI。不要只輸出單一巨大檔案，不要使用偽程式碼。實際執行語法檢查與核心函式 smoke test。
```

<a id="prompt-05"></a>
## Prompt 05：書店資料儀表板（Dash）

```text
你是 Dash/Plotly 資料產品工程師與 UI 設計師。請將以下 Playwright 爬蟲專案升級為「線上書店資料探索儀表板」：
playwright/實戰專案/專案05_線上書店資料擷取/main.py

保留 Books to Scrape 的真實分頁擷取；核心函式只負責回傳資料。將 scrape_books 改成可傳入頁數、類別與 timeout，並回傳正規化資料：price 必須另有可計算的數值欄位，rating 要轉成 1～5。CSV 與 XLSX 匯出功能由這次 AI 賦能新增。

儀表板需求：
1. 現代化編輯風格，淺色背景、白色卡片、深藍文字與琥珀色重點，行動裝置能自動疊疊。
2. 左側可設定爬取頁數、類別、價格範圍、評分、關鍵字與排序，有「更新資料」與「匯入既有 CSV/XLSX」。
3. 頂部 KPI：書籍數、平均價格、5 星比例、最高價、爬取耗時。
4. 圖表：價格分佈、星等長條圖、價格 vs. 評分、類別比較；圖表 hover 顯示書名與價格。
5. 下方 DataTable 支援排序、篩選、分頁、選取與外部書籍連結，可下載篩選後 CSV 或 XLSX；不得加入雲端資料庫。
6. 爬蟲不能阻塞 Dash UI，顯示進度與錯誤卡，沒有資料時顯示明確空狀態。

請使用清楚的 core/services/ui 分層，直接建立完整可執行程式、requirements、README 與核心資料轉換測試。保留只顯示資料的 CLI，將 CSV/XLSX 匯出放在 UI 服務層，完成後執行 smoke test。
```

<a id="prompt-06"></a>
## Prompt 06：網頁互動巡檢桌面工具（PySide6 + PyQtGraph）

```text
你是專業 Qt 桌面應用工程師與 Playwright 自動化專家。請用 PySide6 + PyQtGraph 將以下專案製作成可用於教室展示的「網頁互動巡檢台」：
playwright/實戰專案/專案06_進階互動巡檢/main.py

先把 hover、keyboard、scroll、upload、download 各自拆成獨立可執行、可報告的步驟，並保留 The Internet 真實網站互動。

介面需求：
1. 1440x900 專業桌面佈局：左側測試清單、中央執行時間線與日誌、右側詳細資訊/截圖，底部是總進度。
2. 每個步驟可勾選，顯示尚未執行、執行中、成功、失敗、略過；支援全部執行、單步執行、停止與重設。
3. 可選擇上傳檔案與下載資料夾，不要把路徑寫死。下載完成後可直接開啟所在資料夾。
4. PyQtGraph 即時曲線顯示每步耗時與累計耗時，執行後可比較最慢步驟。
5. Playwright 放在 QThread/worker object，使用 Signal/Slot 回報進度；不能直接由 worker 操作 QWidget，不能凍結介面。
6. 提供深色/淺色 theme、鍵盤快捷鍵、一致 icon、高對比狀態顏色、有意義的空狀態與確認對話框。
7. 可匯出單次 HTML 巡檢報告，包含時間、步驟、結果、耗時、錯誤與成果路徑；不建立歷史資料庫。

請建立模組化、完整可執行的程式，附 requirements、README、uv 執行指令與核心測試。若環境必須使用 PySide5，請在 README 另列相容調整，但預設實作 PySide6。完成後執行 smoke test。
```

<a id="prompt-07"></a>
## Prompt 07：瀏覽器互動實驗室（Flask）

```text
你是 Flask 全端工程師與自動化測試教學設計師。請將以下 popup、alert、iframe 專案升級成一個「瀏覽器互動實驗室」網站：
playwright/實戰專案/專案07_多視窗與iframe/main.py

使用 Flask + Jinja2 + 原生 CSS/JavaScript。將三種 Playwright 操作拆成獨立 service，必須真正連線 The Internet 測試網站，不要以假結果代替。

畫面要求：
1. 以三張大型實驗卡呈現「新分頁 popup」、「JavaScript dialog」、「iframe 內容」，卡片有概念說明、執行按鈕、預期結果與即時狀態。
2. Dialog 卡可選 alert/confirm/prompt 與 accept/dismiss，prompt 可輸入回答；若目標頁不支援某種組合，明確禁用並說明。
3. 每次執行顯示 Playwright 關鍵 API、執行時間線、擷取文字、最終 URL 與截圖，讓學生能對照程式。
4. 使用 SSE 更新狀態；後台任務不阻塞請求，同一個使用者同時只能有一個實驗。
5. 加入「原理」抽屜，以簡短程式碼片段說明 expect_popup、dialog event、frame_locator，但不要把完整程式重複顯示在頁面。
6. 可下載一份含三項結果的 HTML 實驗報告。
7. 結果只保留在本次 session，不建立 CSV、XLSX 或資料庫。

介面要響應式、無障礙、有 loading/success/error/empty 狀態。請直接建立完整檔案、requirements、README 與測試，保留原本 CLI，完成後執行 smoke test。
```

<a id="prompt-08"></a>
## Prompt 08：網頁存證作品庫（Streamlit）

```text
你是 Streamlit 產品工程師、視覺設計師與 Playwright 專家。請將以下截圖、錄影、PDF 專案製作成「網頁存證作品庫」：
playwright/實戰專案/專案08_網頁存證報告/main.py

保留真實 Wikipedia 擷取、整頁/元素/區域截圖、video 與 PDF，將核心邏輯重構為 capture_report(config) 並回傳結構化成果。

介面需求：
1. 左側設定 URL、viewport、整頁截圖、標題截圖、區域截圖、PDF、錄影、檔名前綴與 timeout。
2. 頂部有「建立存證」按鈕與執行進度；主畫面為精緻的作品集網格，可切換圖片、影片、PDF、全部。
3. 成果卡顯示預覽、類型、建立時間、檔案大小、viewport、來源 URL，有下載與開啟按鈕。
4. 圖片有 lightbox，video 可播放，PDF 可下載並顯示第一頁預覽；若 PDF 預覽需額外套件，要正確列入依賴。
5. 支援選取多個成果後打包 ZIP 下載。使用本機 SQLite 記錄來源 URL、類型、檔名、建立時間與大小；不把圖片或影片 blob 寫進資料庫。刪除要有確認，只能刪除專案 output 內檔案及對應索引。
6. 使用 session_state 管理任務與篩選狀態，防止 Streamlit rerun 重複啟動 Playwright。

請建立 app.py、capture service、artifact repository、requirements、README 與路徑安全測試。不使用 base64 假圖或假報告。保留 CLI，完成後執行 smoke test。
```

<a id="prompt-09"></a>
## Prompt 09：API 監聽與 Mock 平台（FastAPI）

```text
你是 FastAPI 後端架構師與 Playwright 網路測試專家。請將以下 JSONPlaceholder request/response/route 專案建立成「API 監聽與 Mock 服務」：
playwright/實戰專案/專案09_API監聽與Mock/main.py

請先重構核心邏輯，提供以下 API：
- POST /runs/real：執行真實 API 請求監聽。
- POST /runs/mock：接受 status code、headers、delay 與 JSON body，用 Playwright route 產生 Mock。
- GET /runs/{id}：取得狀態、請求、回應、時間與錯誤。
- GET /runs：取得最近執行紀錄。
- DELETE /runs/{id}：只刪除本機紀錄。

技術與介面要求：
1. 使用 Pydantic 建立完整 request/response schema、Enum 與驗證，回應狀態碼正確，有一致錯誤格式。
2. Playwright 使用 async API，必須處理啟動、關閉、timeout 與 concurrency limit，不可在 event loop 中使用 sync API。
3. 利用 FastAPI 自動 OpenAPI/Swagger 作為第一個互動介面，為每個 endpoint 撰寫繁體中文 summary、description、範例值與可能錯誤。
4. 另用 FastAPI Jinja2 提供一個輕量 `/dashboard`，左側可編輯 Mock JSON/status/delay，右側比較真實與 Mock 的 request/response、耗時與 diff。
5. Dashboard 要有 JSON 語法驗證、格式化、複製、範例載入、loading、錯誤卡與執行紀錄。
6. 預設僅綁定 127.0.0.1，說明這是本機教學工具；不允許任意目標 URL，避免做成 SSRF 工具。
7. 加入 pytest + FastAPI TestClient 的 schema、validation、route 與錯誤測試。
8. 使用本機 SQLite 保存最多 100 筆執行摘要，啟動時自動建表，DELETE 只刪本機紀錄；不得連線雲端資料庫。

請直接建立完整檔案、requirements、README、uvicorn 執行指令與 curl 範例。保留原本 CLI 範例，完成後執行測試與 API smoke test。
```

<a id="prompt-10"></a>
## Prompt 10：登入狀態管理器（PySide6）

```text
你是重視安全的 PySide6 桌面應用工程師與 Playwright 專家。請將以下 SauceDemo storage state 專案改造為「登入狀態管理器」：
playwright/實戰專案/專案10_登入狀態保存/main.py

保留原本登入、storage_state 儲存、新 context 重用與驗證流程，將它拆成 create_state、validate_state、inspect_state、delete_state 函式。

介面需求：
1. 專業桌面管理工具風格，左側是狀態檔清單，右側是詳情、操作與安全警告，頂部有「新增登入狀態」。
2. 新增對話框含使用者名、密碼、headless 與 timeout；密碼使用 password echo mode，不存檔、不顯示在 log、不寫入例外訊息。
3. 狀態卡顯示建立時間、最後驗證、有效/失效、Cookie 數、localStorage key 數、檔案大小；不直接顯示 Cookie value。
4. 可執行驗證、用該狀態開啟測試頁、重新登入、匯出摘要、刪除。刪除要確認，只能處理專案 output 目錄。
5. Playwright 必須在 QThread 執行，使用 Signal/Slot 更新狀態。同一時間只執行一個登入任務。
6. 加入明顯教學警告：auth.json 含敏感狀態，必須被 .gitignore 排除，不可分享。程式啟動時自動檢查 .gitignore。
7. 有深色/淺色主題、錯誤摘要、空狀態、最後操作日誌與鍵盤快捷鍵。
8. 不使用 CSV、XLSX 或 SQLite 保存 Cookie、storage state 或密碼；auth.json 仍只放在受控的本機 output 目錄。

請建立完整模組化程式、requirements、README 與安全相關測試，保留 CLI。不得將練習帳密當作原始碼常數新增到 GUI。完成後執行 smoke test。
```

<a id="prompt-11"></a>
## Prompt 11：禮貌爬蟲設定助理（Gradio）

```text
你是 Gradio 應用工程師、網路協定教學者與負責任爬蟲專家。請將以下 HTTPBingo 專案製作成「禮貌爬蟲設定助理」：
playwright/實戰專案/專案11_禮貌爬蟲/main.py

核心仍要真正讀取 HTTPBingo robots.txt 與 headers，並回傳 User-Agent、Accept-Language、viewport、locale、timezone、請求間隔與 robots.txt 觀察。不要加入隱藏 webdriver、繞過 CAPTCHA、代理輪替或指紋偽裝功能。

介面要求：
1. gr.Blocks 雙欄佈局，左側是身分與速率設定，右側是「網站實際看到的資訊」與 robots.txt。
2. 可輸入誠實的 bot 名稱、聯絡資訊、locale、timezone、viewport、Accept-Language 與 1～10 秒請求間隔。不允許 1 秒以下。
3. 將預計送出的 headers 與實際回傳 headers 並排比較，用狀態標籤標示一致/不一致。
4. robots.txt 以 code viewer 顯示，另用簡單表格列出 User-agent、Allow、Disallow、Crawl-delay；沒有某欄位時顯示「未指定」，不要自行假設。
5. 頁面上方有綠色原則卡：識別自己、讀取規範、限制速度、只取必要資料；紅色禁止卡：不繞過驗證、不攻擊、不蒼集個資。
6. 可下載單次 CSV 檢查報告，包含設定、實際值、robots.txt 摘要與時間；不建立歷史資料庫。

請建立完整 app.py、核心 service、requirements、README 與 parser/input validation 測試。保留 CLI，介面使用繁體中文、無障礙顏色與友善錯誤。完成後執行 smoke test。
```

<a id="prompt-12"></a>
## Prompt 12：平行爬取效能儀表板（Dash）

```text
你是 Python 效能工程師、Dash/Plotly 儀表板專家與 Playwright async 專家。請將以下平行爬取專案製作成「Playwright 效能實驗儀表板」：
playwright/實戰專案/專案12_平行爬取優化/main.py

保留 async_playwright、多 context、擋圖片/字型/媒體與重試。核心爬蟲只回傳結果；由這次 AI 賦能新增 benchmark 儲存服務。重構為可執行「串行」與「平行」實驗的 service，記錄每個類別的數量、耗時、重試次數、錯誤、擋截資源數，並在可行時記錄 process memory。

儀表板需求：
1. 左側實驗設定：書籍類別多選、並行數 1～5、資源阻擋開關、timeout、重試次數、比較串行與平行。
2. 頂部 KPI：總書數、平行耗時、串行耗時、加速比、成功率、重試數。
3. Plotly 圖表：串行/平行長條比較、每類別 Gantt 時間線、並行數 vs. 耗時、累計書數曲線、可選的記憶體曲線。
4. 執行中有整體進度、各類別狀態與取消按鈕；取消必須正確關閉 page/context/browser。
5. 使用本機 SQLite 保存最多 20 筆實驗摘要，可選取兩筆比較，並可匯出 CSV；不必保存完整書籍清單，不得使用雲端資料庫。
6. 用教學卡解釋「並行不一定越多越快」、網站限制、記憶體與速度的 trade-off，不鼓勵無限提高 concurrency。
7. Dash callback 不能用 asyncio.run 產生嵌套 event loop 問題；請設計清楚的 async worker 邊界與關閉機制。

請建立完整模組化程式、requirements、README、benchmark 單元測試與少量 smoke test。保留原本只顯示摘要的 CLI，不使用假的效能數字。
```

---

## 學生使用 AI 後的驗收清單

- [ ] 我能指出 UI 入口檔與 Playwright 核心模組。
- [ ] 我能說明輸入值如何傳到 Playwright，以及結果如何回到介面。
- [ ] 介面執行 Playwright 時不會凍結，也不會重複啟動無限個瀏覽器。
- [ ] loading、成功、空資料、timeout、網路失敗都有清楚畫面。
- [ ] 輸出檔是真正由 Playwright 產生，不是 AI 放入的靜態假資料。
- [ ] 密碼、Cookie、storage state 與私人資料沒有被寫入 Git、日誌或介面。
- [ ] 原本 CLI 仍可執行，新 UI 也有明確安裝與啟動指令。
- [ ] 我實際執行過主要流程，並能解釋至少一個 AI 產生後由我修正的問題。

[ ← 返回第十三章](README.md)
