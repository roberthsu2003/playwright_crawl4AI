# Playwright & Crawl4AI 爬蟲教學

> 這份講義涵蓋現代網路爬蟲的核心技術，從基礎到實戰應用

## 📚 目錄

- [快速開始](#快速開始)
- [為什麼要學現代爬蟲](#為什麼要學現代爬蟲)
- [Webwright](./webwright/README.md) | [使用 Webwright 進行快速自動化](./webwright/README.md)
- [Playwright 課程](#playwright-課程)
- [Crawl4AI 課程](#crawl4ai-課程)
- [Playwright vs Crawl4AI 比較](#playwright-vs-crawl4ai-比較)
- [實際案例](#實際案例)
- [學習建議](#學習建議)
- [官方資源](#官方資源)

---

## 快速開始

### 建議學習路徑

1. **學習 Asyncio 非同步編程** → [Asyncio 教學](./asyncio套件教學/)（⚠️ 學 Crawl4AI 前必讀）
2. **先學 Playwright 基礎** → [開始 Playwright 學習](./playwright/第01章_Playwright簡介/README.md)
3. **再學 Crawl4AI 進階** → [開始 Crawl4AI 學習](#Crawl4AI-課程)

### 環境需求

- Python 3.8+ (建議 3.10+)
- 穩定的網路連線
- 硬碟空間至少 2GB

### 安裝步驟

#### uv+pyproject.toml 環境
```bash
uv sync
uv run playwright install chromium #安裝chromium,是安裝在電腦,非虛擬環境
uv run playwright install firefox #安裝firefox,是安裝在電腦,非虛擬環境
uv pip install --upgrade crawl4ai #安裝和更新crawl4ai,是安裝在虛擬環境
uv run crawl4ai-setup #執行crawl4ai後續設定
uv run crawl4ai-doctor #檢查crawl4ai是否安裝成功
```

#### 一般環境

```bash
# 1. 安裝 Playwright
pip install playwright
playwright install  # ⚠️ 重要：下載瀏覽器驅動

# 2. 安裝 Crawl4AI
pip install crawl4ai

# 3. Run post-installation setup
crawl4ai-setup

# 4.Verify your installation
crawl4ai-doctor
```


詳細安裝說明：
- [Playwright 安裝指南](./playwright/第01章_Playwright簡介/README.md)
- [Crawl4AI 安裝指南](./crawl4AI/安裝/README.md)

### 前置知識

- 基本的 Python 語法（變數、迴圈、函式）
- 知道 HTML 長什麼樣子（不用很精通，看得懂標籤就好）
- 會用命令列（terminal）執行指令

---

## 為什麼要學現代爬蟲？

### 傳統爬蟲的困境

- ❌ **JavaScript 產生的內容抓不到** - 現在很多網站用 React、Vue 這些框架，資料都是靠 JavaScript 動態載入的
- ❌ **反爬蟲機制越來越強** - User-Agent 檢查、Cookie 追蹤、行為分析...隨便一個擋住你就爬不動了
- ❌ **等待時間很難控制** - 頁面載入有快有慢，要用 `time.sleep()` 猜時間，不然就漏資料
- ❌ **處理動態內容很麻煩** - 像是下拉選單、無限滾動、彈出視窗...傳統方法很難處理

### 現代爬蟲的優勢

- ✅ **真的瀏覽器引擎** - 不是模擬，而是用真正的 Chromium/Firefox，JavaScript 跑得跟真人瀏覽一樣
- ✅ **自動等待機制** - 不用猜時間，程式會等到元素真的出現才繼續
- ✅ **反爬蟲對策內建** - 模擬真實使用者行為，降低被擋的機率
- ✅ **AI 輔助提取** - Crawl4AI 可以搭配 LLM 智能解析網頁結構，不用手寫複雜的選擇器

簡單來說，**傳統爬蟲像是「照照片」**，只能看到拍那瞬間的畫面；**現代爬蟲像是「真的在用瀏覽器」**，可以看到完整的互動過程。

---

## Webwright

[查看 Webwright 使用說明](./webwright/README.md)

- 是整合在 Claude Code 中、基於 Playwright 的**網頁自動化助手**。它能讓您用**自然語言**來指揮瀏覽器執行各種操作，並以「程式即動作（code-as-action）」的模式完成任務。

### 主要特色：
- 🤖 **自然語言操作**：不需要手寫複雜的 Python 腳本，只需用中文或英文描述您的需求（例如：「前往 Google 搜尋特定關鍵字並擷取前三名網址」），它就會自動編寫代碼並操作瀏覽器。
- 📸 **自動截圖存證**：在執行每個關鍵步驟時，會自動截圖並保存至 `final_runs/run_<id>/` 目錄，方便驗證執行結果與排錯。
- ⚙️ **支援兩種模式**：
  - `/webwright`：用於快速執行一次性的網頁自動化或爬蟲任務。
  - `/webwright:craft`：用來封裝、製作可重複使用的參數化爬蟲腳本。

---

## Playwright vs Crawl4AI 比較

### 核心差異對比

| 比較項目 | Playwright | Crawl4AI |
|---------|-----------|----------|
| **原始設計目的** | 自動化測試工具 | 專門的爬蟲框架 |
| **爬蟲功能** | ✅ 完全支援（需自己寫邏輯） | ✅ 完全支援（內建爬蟲功能） |
| **底層技術** | 直接控制瀏覽器 | 基於 Playwright 封裝 |
| **學習曲線** | 需要理解底層原理 | 上手較快，API 更簡潔 |
| **控制精細度** | 非常精細，完全掌控 | 較高層次，專注資料提取 |
| **非同步處理** | 需自己實作 | 內建非同步批次處理 |
| **AI 整合** | 需自己串接 | 內建 LLM 解析功能 |
| **程式碼量** | 較多（需處理細節） | 較少（框架處理細節） |

### 使用場景建議

#### 選擇 Playwright

- 需要很精細的控制（像是測試網站功能）
- 想要完全理解底層的運作原理
- 只是爬幾個簡單的網站
- 需要客製化特殊的瀏覽器行為

#### 選擇 Crawl4AI

- 要爬很多網頁、處理大量資料
- 網站結構很複雜，想用 AI 幫忙解析
- 想要快速開發，不想處理太多細節
- 需要非同步批次爬取多個網站

### 我的建議

**先學 Playwright 打基礎**，理解瀏覽器自動化的原理。之後再用 Crawl4AI 提升開發效率。

兩者不衝突，Crawl4AI 內部就是用 Playwright，所以你學的 Playwright 知識完全不會浪費。就像學會開手排車之後，開自排車會更得心應手。

### 簡單比喻

- **Playwright** = 瑞士刀（多功能工具，測試和爬蟲都能做，但需要自己組裝）
- **Crawl4AI** = 專業爬蟲工具組（只做爬蟲，但做得更快更方便）

---


## Playwright 課程

**官方網站**: [https://playwright.dev/](https://playwright.dev/)

### 什麼是 Playwright？

Playwright 是微軟開發的網頁自動化工具。雖然原本是設計給自動化測試用的，但因為它能完整模擬真實瀏覽器行為，所以也是非常強大的爬蟲工具。

### 為什麼要學 Playwright？

- **真的支援多瀏覽器** - Chromium、Firefox、WebKit 都可以用同一套 API
- **自動等待機制** - 不用自己寫 `time.sleep()`，它會自動等到元素出現
- **功能很完整** - 截圖、錄影、攔截網路請求、處理 Cookie...該有的都有
- **速度很快** - 官方宣稱比 Selenium 快 2-3 倍，實際用起來確實有感

### 課程章節

| 章節 | 內容 | 重點 |
|------|------|------|
| [第 1 章](./playwright/第01章_Playwright簡介/) | Playwright 簡介 | 了解它是什麼、怎麼安裝 |
| [第 2 章](./playwright/第02章_基礎操作/) | 基礎操作 | 啟動瀏覽器、開啟網頁、點擊按鈕 |
| [第 3 章](./playwright/第03章_元素定位/) | 元素定位 | CSS 選擇器、XPath、Playwright 內建定位器 |
| [第 4 章](./playwright/第04章_等待與同步/) | 等待與同步 | ⭐ 重點章節，一定要搞懂等待機制 |
| [第 5 章](./playwright/第05章_資料擷取/) | 資料擷取 | 怎麼把網頁上的文字、連結、屬性抓下來 |
| [第 6 章](./playwright/第06章_進階互動/) | 進階互動 | 滑鼠拖曳、鍵盤操作、滾動頁面 |
| [第 7 章](./playwright/第07章_多頁面與框架處理/) | 多頁面處理 | 處理多個分頁、彈出視窗、iframe |
| [第 8 章](./playwright/第08章_截圖與錄影/) | 截圖與錄影 | 頁面截圖、操作過程錄影、存成 PDF |
| [第 9 章](./playwright/第09章_網路請求與回應/) | 網路請求 | 攔截 API 請求、查看回應內容 |
| [第 10 章](./playwright/第10章_登入與Cookie處理/) | 登入處理 | 自動登入網站、管理 Cookie 保持登入狀態 |
| [第 11 章](./playwright/第11章_反爬蟲對策/) | 反爬蟲對策 | 怎麼避免被網站擋掉 |
| [第 12 章](./playwright/第12章_效能優化/) | 效能優化 | 讓爬蟲跑得更快、更省資源 |
| [第 13 章](./playwright/第13章_實戰專案/) | 實戰專案 | 用前面學的知識寫幾個完整的爬蟲 |

---

## Crawl4AI 課程

**官方網站**: [https://github.com/unclecode/crawl4ai](https://github.com/unclecode/crawl4ai)

### 什麼是 Crawl4AI？

Crawl4AI 是一個**專門為爬蟲設計的框架**，建立在 Playwright 之上，把常見的爬蟲任務簡化。它不是測試工具，而是純粹的爬蟲框架。

### 為什麼要用 Crawl4AI？

雖然 Playwright 已經很強了，但用它寫爬蟲時，每次都要處理很多重複的邏輯：

**用 Playwright 寫爬蟲**（需要自己處理所有細節）：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    # 要自己寫等待邏輯
    # 要自己寫資料提取邏輯
    # 要自己處理錯誤重試
    # 要自己管理瀏覽器生命週期
    browser.close()
```

**用 Crawl4AI 寫爬蟲**（框架處理細節，你專注資料）：
```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url='https://example.com')
    # 框架自動處理等待、重試、資料提取
    print(result.markdown)  # 直接拿到清理好的資料
```

### 核心特色

- **專為爬蟲設計** - 從頭到尾就是為爬蟲打造的
- **非同步處理** - 可以同時爬多個網頁，速度比傳統的 for 迴圈快很多
- **內建 Playwright** - 你不需要另外啟動瀏覽器，它都幫你處理好了
- **AI 驅動提取** - 可以請 LLM 幫你分析網頁，找出資料在哪裡
- **Schema 設計** - 用 CSS Schema 定義要抓的資料結構，很直觀

### 課程章節

| 章節 | 內容 | 重點 |
|------|------|------|
| [Asyncio 教學](./crawl4AI/asyncio套件教學/) | Python 非同步編程 | ⚠️ **重要：學 Crawl4AI 前必讀** |
| [初體驗](./crawl4AI/初體驗/) | 第一個 Crawl4AI 程式 | 快速上手，感受差別 |
| [快速入門](./crawl4AI/Crawl4A快速入門/) | 基本配置和內容過濾 | 學會基礎設定和資料抓取 |
| [CSS Schema](./crawl4AI/Crawl4A快速入門/手動方式產生css_schema/) | 手動定義資料結構 | 不用 LLM 的方法 |
| [JavaScript 操控](./crawl4AI/Crawl4A操控javascript/) | 處理動態內容 | 滾動、點擊、等待操作 |
| [多頁面爬蟲](./crawl4AI/Crawl4A多頁面爬蟲/) | 批次爬取多個網頁 | 使用 `arun_many()` 加速 |
| [排程任務](./crawl4AI/排程/) | 定時自動執行 | 讓爬蟲在背景執行 |
| [實際案例](./crawl4AI/實際案例/) | 完整的真實專案 | 匯率、股票資訊、GUI 應用 |

### ⚠️ 重要：先學 Asyncio

Crawl4AI 大量使用非同步編程，所以**一定要先看懂 asyncio**。如果 `async/await` 對你來說很陌生，建議先看這篇：

→ [Python Asyncio 非同步編程教學](./crawl4AI/asyncio套件教學/)

---



## 實際案例

講義裡有幾個完整的專案可以參考：

### 1. 台灣銀行牌告匯率（入門）
- **資料夾**: [1台灣銀行牌告匯率](./crawl4AI/實際案例/1台灣銀行牌告匯率/)
- **類型**: 靜態網頁爬蟲
- **技術**: CSS Schema 資料擷取、定時更新
- **適合**: 剛入門的時候看
- **難度**: ⭐⭐ 初級

### 2. 台灣即時股票資訊（中級）
- **資料夾**: [2台灣即時股票資訊](./crawl4AI/實際案例/2台灣即時股票資訊/)
- **類型**: 動態網頁爬蟲
- **技術**: JavaScript 渲染、動態內容處理、自訂屬性選擇器
- **適合**: 有基礎之後挑戰
- **難度**: ⭐⭐⭐⭐ 中級

### 4. 股票批次爬取 - GUI 版（高級）
- **資料夾**: [4台灣即時股票資訊_tkinter](./crawl4AI/實際案例/4台灣即時股票資訊_tkinter/)
- **類型**: 功能完整的爬蟲工具（AI 輔助開發）
- **技術**: 雙模式運行（命令列 + GUI）、批次爬取、進度顯示
- **特色**: 股票搜尋、全選功能、即時進度
- **適合**: 學習批次處理與實用工具開發
- **難度**: ⭐⭐⭐⭐⭐ 高級

> 💡 **提示**：專案 3 和 4 都是 AI 輔助開發的完整專案，包含需求文件（PRD.md）與完整說明，適合學習 AI 輔助開發流程。

> 💡 **提示**：先專案4再專案3 

### 3. 股票即時監控 - GUI 版（高級）
- **資料夾**: [3台灣即時股票資訊_tkinter](./crawl4AI/實際案例/3台灣即時股票資訊_tkinter/)
- **類型**: 完整桌面應用程式（AI 輔助開發）
- **技術**: Tkinter GUI、即時監控、自動更新、多執行緒
- **特色**: 視覺化顯示（紅漲綠跌）、搜尋功能
- **適合**: 學習 GUI 整合與即時監控系統
- **難度**: ⭐⭐⭐⭐⭐ 高級

> 💡 **提示**：專案 3 和 4 都是 AI 輔助開發的完整專案，包含需求文件（PRD.md）與完整說明，適合學習 AI 輔助開發流程。

---

## **AI整合方向**

| **類型**              | **工具**                 | **適合做什麼**                        | **教學難度** |
| ------------------- | ---------------------- | -------------------------------- | -------- |
| 桌面版                 | Tkinter                | 關鍵字搜尋、按鈕啟動爬蟲、匯出 CSV              | 低        |
| 網頁版                 | Streamlit              | 爬蟲結果查詢、表格、圖表、下載報表                | 低        |
| 網頁版 GUI             | NiceGUI                | 比 Streamlit 更像一般後台系統，有按鈕、表單、頁面   | 中        |
| API 服務              | FastAPI                | 把 Playwright 爬蟲包成 API，前端或其他程式可呼叫 | 中        |
| 排程任務                | schedule / APScheduler | 每天自動爬資料，例如股價、匯率、公告               | 中        |
| 資料儲存                | SQLite / PostgreSQL    | 把爬蟲結果存起來，做歷史查詢                   | 中        |
| 報表輸出                | pandas + openpyxl      | 匯出 Excel、產生統計報表                  | 低        |
| LINE / Telegram Bot | Bot API                | 查詢爬蟲結果、推播價格變化                    | 中        |
| AI 分析               | OpenAI / Gemini API    | 將爬到的資料摘要、分類、產生報告                 | 中高       |

---

## 官方資源

### Playwright
- [官方網站](https://playwright.dev/)
- [Python 版本文件](https://playwright.dev/python)
- [API 參考](https://playwright.dev/python/docs/api/class-playwright)
- [快速入門](https://playwright.dev/python/docs/intro)
- [疑難排解](https://playwright.dev/python/docs/troubleshooting)

### Crawl4AI
- [GitHub 官方倉庫](https://github.com/unclecode/crawl4ai)
- [原始碼和 Issue](https://github.com/unclecode/crawl4ai/issues)
- [使用範例](https://github.com/unclecode/crawl4ai/tree/main/examples)



