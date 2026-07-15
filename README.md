# Playwright & Crawl4AI 爬蟲教學

> 這份講義涵蓋現代網路爬蟲的核心技術，從基礎到實戰應用

## 📚 目錄

- [🚀 快速開始](#快速開始)
- [💡 為什麼要學現代爬蟲？](#為什麼要學現代爬蟲)
- [🤖 Webwright 自動化助手](#webwright) (📄 [使用說明](./webwright/README.md))
- [⚖️ Playwright vs Crawl4AI 比較](#playwright-vs-crawl4ai-比較) (📄 [完整對比文件](./docs/comparison.md))
- [🎭 Playwright 課程](#playwright-課程) (📄 [完整課程大綱](./playwright/README.md))
- [🤖 Crawl4AI 課程](#crawl4ai-課程) (📄 [完整課程大綱](./crawl4AI/README.md))
- [📈 實際案例](#實際案例) (📄 [專案詳情與難度說明](./docs/cases.md))
- [⚡ AI 整合方向](#ai整合方向) (📄 [整合工具與難度表](./docs/ai_integration.md))
- [🌐 官方資源](#官方資源)

---

## 快速開始

### 建議學習路徑

1. **學習 Asyncio 非同步編程** → [Asyncio 教學](./asyncio套件教學/)（⚠️ 學 Crawl4AI 前必讀）
2. **先學 Playwright 基礎** → [開始 Playwright 學習](./playwright/第01章_Playwright簡介/README.md)
3. **再學 Crawl4AI 進階** → [開始 Crawl4AI 學習](#crawl4ai-課程)

### 環境需求

- Python 3.8+ (建議 3.10+)
- 穩定的網路連線
- 硬碟空間至少 2GB

### 安裝步驟

#### uv+pyproject.toml 環境
```bash
uv add playwright crawl4ai
uv sync
uv run playwright install chromium #安裝chromium,是安裝在電腦,非虛擬環境
uv run playwright install firefox #安裝firefox,是安裝在電腦,非虛擬環境
```

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

Playwright 與 Crawl4AI 在定位上有所不同：Playwright 是功能強大的**網頁自動化測試工具**，而 Crawl4AI 是專門為資料抓取與 LLM 優化的**專業爬蟲框架**。

完整的核心差異對比表格、使用場景建議以及簡單比喻，請參閱：
👉 [Playwright vs Crawl4AI 比較文件](./docs/comparison.md)

---

## Playwright 課程

Playwright 是由微軟開發的現代網頁自動化工具。因為它能完整模擬真實瀏覽器行為，自動等待元素，並且支援多個瀏覽器引擎，因此是現代動態爬蟲的必學工具。

- **官方網站**: [Playwright 官方網站](https://playwright.dev/)
- **課程大綱**: 包含基礎操作、元素定位、等待機制、多頁面處理、反爬蟲對策以及效能優化等 13 個完整章節。
- **實戰專案**: 維基百科搜尋器、台灣高鐵時刻表查詢、PTT 熱門文章爬蟲。

詳細的章節列表與學習路徑，請參閱：
👉 [Playwright 完整教學講義](./playwright/README.md)

---

## Crawl4AI 課程

Crawl4AI 是基於 Playwright 封裝的非同步爬蟲框架，專為需要批次爬取、資料清理以及與 AI (LLM) 整合的任務所設計。它自動化處理了大量的瀏覽器生命週期與重試細節，讓您能以最少程式碼快速取得乾淨的 Markdown 格式資料。

- **官方網站**: [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)
- **課程大綱**: 包含初體驗、CSS Schema 資料結構手動定義、JS 動態操作、非同步批次處理 (`arun_many()`) 等課程。
- **前置準備**: 由於該框架大量使用非同步編程，**必須**先學會 Python 的 `async/await` 機制。

詳細的範例代碼、特色說明與課程章節，請參閱：
👉 [Crawl4AI 完整教學講義](./crawl4AI/README.md)

---

## 實際案例

本教學中收錄了多個實際的專案，幫助您從基礎的靜態網頁抓取，一步步挑戰至多執行緒、AI 協同開發的 GUI 監控軟體：

1. **台灣銀行牌告匯率**（⭐⭐ 初級）：學習 CSS Schema 與定時排程。
2. **台灣即時股票資訊**（⭐⭐⭐⭐ 中級）：學習動態網頁渲染與精準定位。
3. **股票批次爬取 - GUI 桌面版**（⭐⭐⭐⭐⭐ 高級）：學習 Tkinter 介面整合與並發控制。
4. **股票即時監控 - GUI 桌面版**（⭐⭐⭐⭐⭐ 高級）：學習多執行緒、即時刷新與自動更新。

每個案例的檔案路徑與技術重點說明，請參閱：
👉 [爬蟲實戰案例與專案說明](./docs/cases.md)

---

## AI 整合與應用拓展方向

當您掌握爬蟲技術後，可以將其與多種工具和框架整合，例如：
- **桌面版 GUI** (Tkinter)
- **網頁版 GUI / 後台** (Streamlit, NiceGUI)
- **API 服務** (FastAPI)
- **資料庫與排程** (PostgreSQL, APScheduler)
- **AI 智慧分析** (OpenAI / Gemini API)

有關整合難度表與適合的應用場景，請參閱：
👉 [AI 整合與應用拓展方向](./docs/ai_integration.md)

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
- [原始碼 and Issue](https://github.com/unclecode/crawl4ai/issues)
- [使用範例](https://github.com/unclecode/crawl4ai/tree/main/examples)
