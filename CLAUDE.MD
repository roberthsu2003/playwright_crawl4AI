# CLAUDE.MD - Project Context & System Instructions

## 核心回覆語言規範 (Critical Language Instruction)
- **無論使用者是以英文或繁體中文輸入，AI 必須一律以「繁體中文（Traditional Chinese）」進行回覆。**
- 專案內的所有文件說明、程式碼註解也應以繁體中文為主。

---

## 專案架構概覽 (Project Architecture)

本專案是一個教學與實戰導向的 Python 爬蟲專案，主要整合了以下三大核心技術：

1. **Playwright (微軟瀏覽器自動化工具)**
   - 用於模擬真實瀏覽器行為，支援 Chromium、Firefox 及 WebKit。
   - 處理動態 JavaScript 渲染、網頁點擊、表單填寫、截圖與錄影等基礎操作。
   - 課程位於 `playwright/課程章節/`，專案位於 `playwright/實戰專案/`。

2. **Crawl4AI (AI 驅動的非同步爬蟲框架)**
   - 基於 Playwright 封裝的高階爬蟲框架，專為大規模、結構化資料抓取設計。
   - 支援非同步批次處理 (`arun_many`) 與 LLM 智慧解析網頁結構。
   - 課程位於 `crawl4AI/課程章節/`，專案位於 `crawl4AI/實戰專案/`。

3. **Webwright (自然語言網頁自動化助手)**
   - 整合於 AI 助手中的 Playwright 網頁自動化模組。
   - 支援使用自然語言直接操作瀏覽器完成任務（`/webwright`）或製作參數化腳本（`/webwright:craft`）。
   - 相關說明位於 `tools/webwright/` 目錄。

---

## 虛擬環境與套件管理 (UV Virtual Environment)

本專案使用現代 Python 套件管理器 **uv**。**所有開發與執行操作必須在 uv 虛擬環境中進行。**

### 1. 啟用虛擬環境
- **方法 A（推薦）：啟用本機虛擬環境**
  ```bash
  source .venv/bin/activate
  ```
- **方法 B：免啟用直接執行 (使用 `uv run`)**
  若不啟用虛擬環境，可在命令前加上 `uv run` 來確保在虛擬環境的上下文中執行：
  ```bash
  uv run python <腳本路徑>
  ```

### 2. 套件與依賴管理
- **同步依賴**：當變更 `pyproject.toml` 或拉取新代碼時，同步本機虛擬環境：
  ```bash
  uv sync
  ```
- **新增套件**：
  ```bash
  uv add <套件名稱>
  ```
- **移除套件**：
  ```bash
  uv remove <套件名稱>
  ```

### 3. Playwright 與 Crawl4AI 初始化
- **安裝瀏覽器驅動**：
  ```bash
  uv run playwright install
  ```
- **Crawl4AI 初始化與診斷**：
  ```bash
  uv run crawl4ai-setup
  # 檢查安裝狀態
  uv run crawl4ai-doctor
  ```

---

## 常用命令速查 (Cheat Sheet)

### 執行範例程式
- **執行 Playwright 基礎範例**（假設在虛擬環境中或使用 `uv run`）：
  ```bash
  uv run python playwright/課程章節/第02章_基礎操作/index.py
  ```
- **執行 Crawl4AI 實戰案例**：
  ```bash
  uv run python crawl4AI/實戰專案/01_台灣銀行牌告匯率/main.py
  ```

### 啟動 Jupyter Notebook (用於互動式教學)
```bash
uv run jupyter notebook
# 或
uv run jupyter lab
```

---

## 開發規範與約定 (Development Conventions)

### 1. 非同步程式設計 (Asyncio)
- Crawl4AI 範例大量依賴非同步設計，編寫爬蟲時務必使用 `async/await`。
- 在 Jupyter Notebook 中執行非同步代碼時，必須使用 `nest_asyncio`：
  ```python
  import nest_asyncio
  nest_asyncio.apply()
  ```

### 2. 程式碼風格
- **變數與函式命名**：使用英文蛇形命名法 (`snake_case`)。
- **註解**：必須包含繁體中文註解，詳細說明複雜邏輯與爬蟲選擇器定位。
- **錯誤處理**：爬蟲腳本需包含適當的 `try-except` 區塊，以防網頁結構變更導致程式崩潰。

### 3. 反爬蟲友善性
- 合理設置延遲時間，避免頻繁請求導致 IP 被封鎖。
- 在適當場景下使用 User-Agent 偽裝或 Cookie 保持登入狀態。
