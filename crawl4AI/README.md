# Crawl4AI 完整教學講義

**官方網站**: [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)

## 🤖 什麼是 Crawl4AI？

Crawl4AI 是一個**專門為爬蟲與 AI 資料提取設計的開源框架**，它建立在 Playwright 之上，並將常見的網頁爬取與清理邏輯進行了高度封裝。它不是像 Selenium 或 Playwright 那樣的通用網頁自動化測試工具，而是純粹為爬蟲打造的框架。

---

## 💡 為什麼要用 Crawl4AI？

雖然 Playwright 已經非常強大，但用它編寫爬蟲時，您需要手動處理許多重複的底層細節。Crawl4AI 幫您封裝了這些複雜度，讓您可以專注於資料本身。

### 程式碼對比

#### 1. 使用 Playwright 寫爬蟲（需手動處理細節）
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')
    # ⚠️ 需要手動編寫：
    # - 頁面載入等待邏輯
    # - 資料提取與 HTML 清理邏輯
    # - 錯誤重試機制
    # - 瀏覽器與上下文生命週期管理
    content = page.content()
    browser.close()
```

#### 2. 使用 Crawl4AI 寫爬蟲（框架自動處理，專注資料）
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url='https://example.com')
        # ✅ 框架會自動處理等待、重試、反爬蟲，並將網頁轉換為清理好的 Markdown 格式
        print(result.markdown)

asyncio.run(main())
```

---

## ⚡ 核心特色

- **專為爬蟲設計**：開箱即用，預設提供優化過的爬取配置。
- **高併發非同步處理**：內建對 `asyncio` 的支持，可以使用 `arun_many()` 同時高效爬取多個網頁，速度遠快於傳統的序列爬取。
- **自動清理與 Markdown 轉換**：自動去除網頁中的廣告、導航欄等雜訊，直接輸出乾淨的 Markdown，非常適合餵給 LLM 進行後續分析。
- **AI 驅動智能提取**：支援結合 LLM (如 OpenAI, Gemini 等), 利用 Schema 智慧解析網頁結構，無需編寫複雜的 CSS/XPath 選擇器。
- **彈性 Schema 定義**：支援使用 CSS Schema 手動定義想要抓取的欄位與資料結構。

---

## ⚠️ 重要提示：先學 Asyncio 非同步編程

由於 Crawl4AI 深度依賴 Python 的非同步編程機制，在開始學習 Crawl4AI 之前，**強烈建議**您先掌握 `async/await` 與 `asyncio` 的運作方式。如果這對您來說較為陌生，請先閱讀：

👉 [Python Asyncio 非同步編程教學](../asyncio套件教學/)

---

## 📚 課程章節

| 章節 | 內容 | 重點 |
| :--- | :--- | :--- |
| **前置準備** | [Asyncio 教學](../asyncio套件教學/) | ⚠️ **重要：學 Crawl4AI 前必讀的非同步編程基礎** |
| **第一章** | [安裝與配置](./安裝/) | 快速安裝並執行第一個 Crawl4AI 程式，感受其便利性。 |
| **第二章** | [Crawl4AI 初體驗](./初體驗/) | 了解基本配置、請求頭設定與內容過濾器。 |
| **第三章** | [快速入門指南](./Crawl4A快速入門/) | 了解核心配置、Markdown 輸出與不同的資料擷取策略。 |
| **第四章** | [手動定義 CSS Schema](./Crawl4A快速入門/手動方式產生css_schema/) | 學習手動定義資料結構，免去 LLM 的成本與不確定性。 |
| **第五章** | [JavaScript 網頁互動](./Crawl4A操控javascript/) | 處理滾動、點擊、延遲等待等動態網頁內容。 |
| **第六章** | [多網址爬蟲與非同步 Dispatcher](./Crawl4A多頁面爬蟲/) | 批次爬取多個網頁，使用非同步機制大幅提升效率。 |
| **第七章** | [排程與定時任務](./排程/) | 結合排程工具在背景定時自動執行爬蟲任務。 |
| **第八章** | [實際案例](../docs/cases.md) | 完整的真實專案（匯率、股票資訊、GUI 桌面應用）。 |

---

## 課程大綱

### **[前置準備：Asyncio 教學](../asyncio套件教學/)**
- Python 協程與非同步編程基本概念
- `async/await` 語法與 `asyncio.run()` 的調用
- 非同步任務的並行執行

### **[第一章：安裝與配置](./安裝/README.md)**
#### 1.1 安裝 Crawl4AI
- 安裝 `crawl4ai` 與 `nest_asyncio`
- 執行 `playwright install` 初始化瀏覽器
#### 1.2 檢查與設定
- 驗證安裝版本
- 解決 Jupyter Notebook/Windows 等不同環境下的非同步衝突

### **[第二章：Crawl4AI 初體驗](./初體驗/README.md)**
#### 2.1 Playwright 與 Crawl4AI 結合的優勢
- 什麼是 Playwright？為什麼 Crawl4AI 要基於 Playwright？
- 處理動態網頁渲染與自動等待機制
#### 2.2 快速執行第一個 Crawl4AI 爬蟲
- 實作最基礎 of `AsyncWebCrawler`
- 認識爬取結果 `result.markdown` 與其清理特色

### **[第三章：快速入門指南](./Crawl4A快速入門/README.md)**
#### 3.1 Crawl4AI 基礎配置
- 認識 `BrowserConfig` 與 `CrawlerRunConfig` 核心類別
- 深入設定 Header、User-Agent 與內容過濾器
#### 3.2 資料擷取策略
- 手動與 LLM 智慧擷取模式概覽
- 使用 `manual_control_example.py` 進行操作示範

### **[第四章：手動定義 CSS Schema](./Crawl4A快速入門/手動方式產生css_schema/README.md)**
#### 4.1 無 LLM 的資料提取策略
- 為什麼要避免使用 LLM 進行基本提取（成本、延遲、準確性）
- 認識 `JsonCssExtractionStrategy` 與 `JsonXPathExtractionStrategy`
#### 4.2 CSS Schema 定義與實作
- 基礎 CSS 選擇器定義與 base selector 概念
- 複雜與嵌套 (nested) 網頁結構的欄位解析

### **[第五章：JavaScript 網頁互動](./Crawl4A操控javascript/README.md)**
#### 5.1 動態網頁互動
- 執行自訂 JavaScript 代碼 (`js_code`) 與設定 `wait_for` 條件
- 處理「載入更多」按鈕、自動滾動到頁面底部
#### 5.2 複雜流程與 Session 重複使用
- 模擬表單填寫與提交
- 跨多個步驟重複使用 browser session

### **[第六章：多網址爬蟲與非同步 Dispatcher](./Crawl4A多頁面爬蟲/README.md)**
#### 6.1 調度器 (Dispatcher) 機制
- 什麼是 Dispatcher？為什麼多網址爬取需要調度？
- 認識 `MemoryAdaptiveDispatcher` 與 `SemaphoreDispatcher`
#### 6.2 非同步批次處理
- 使用 `arun_many()` 同時高效爬取多個網頁
- 自動調整速度、避免網站封鎖與保護系統資源

### **[第七章：排程與定時任務](./排程/README.md)**
#### 7.1 每分鐘自動執行爬蟲
- 使用 `while True` + `time.sleep` 的基本寫法與缺點
- 利用系統內建的 `cron` (Linux/macOS) 進行定時任務
#### 7.2 排程最佳實踐
- 背景執行爬蟲與記錄 Log 技巧
- 中斷重啟與持久化運作

### **[第八章：實際案例](../docs/cases.md)**
- 匯率、股票資訊與 GUI 桌面應用的整合實戰，包含：
  - 台灣銀行牌告匯率 (初級)
  - 台灣即時股票資訊 (中級)
  - 股票批次爬取 - GUI 桌面版 (高級)
  - 股票即時監控 - GUI 桌面版 (高級)
- 詳細請參閱 👉 [爬蟲實戰案例與專案說明](../docs/cases.md)
