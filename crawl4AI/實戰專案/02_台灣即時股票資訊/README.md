# 台灣即時股票資訊爬蟲

## 專案簡介

這是一個使用 Crawl4AI 框架爬取台灣股票即時資訊的進階專案。本專案示範如何處理動態網頁、JavaScript 互動、以及擷取結構化的股票數據。相較於靜態網頁爬蟲，本專案展示了更複雜的爬蟲技術。

**目標網站**: [玩股網 - 台積電技術分析](https://www.wantgoo.com/stock/2330/technical-chart)

**範例股票**: 台積電 (2330)

## 功能特色

- ✅ 爬取即時股票資訊（價格、漲跌、成交量等）
- ✅ 處理動態網頁內容（JavaScript 渲染）
- ✅ 執行 JavaScript 指令進行頁面互動
- ✅ 使用非 Headless 模式觀察爬蟲過程
- ✅ 完整擷取 10 項股票關鍵指標
- ✅ 結構化 JSON 輸出
- ✅ 繞過快取確保資料即時性

## 環境需求

### Python 版本
- Python 3.8 或以上（建議使用 3.10+）

### 相依套件
```bash
pip install crawl4ai
```

## 專案結構

```
2台灣即時股票資訊/
├── main.py              # 主程式
└── README.md            # 本說明文件
```

## 程式說明

### 核心功能模組

#### 1. 股票資料擷取 Schema

本專案使用 JsonCssExtractionStrategy 定義擷取規則，針對玩股網的 HTML 結構設計。

**擷取的欄位說明**：

| 欄位名稱 | 說明 | CSS 選擇器特點 |
|---------|------|---------------|
| 日期時間 | 股票報價更新時間 | 使用 `time` 標籤與 ID 選擇器 |
| 股票號碼 | 股票代碼（如 2330） | 使用自訂屬性 `c-model='id'` |
| 股票名稱 | 公司名稱（如台積電） | 使用 `h3` 標籤與自訂屬性 |
| 即時價格 | 當前成交價格 | 在 `quotes-info` 區塊內的 `deal` 類別 |
| 漲跌 | 與前一日收盤價的價差 | 使用 `chg` 類別 |
| 漲跌百分比 | 漲跌幅度百分比 | 使用 `chg-rate` 類別 |
| 開盤價 | 當日開盤價格 | 使用複雜的自訂屬性選擇器 |
| 最高價 | 當日最高價格 | 使用 `c-model-dazzle` 屬性 |
| 成交量(張) | 當日成交量 | 使用 `c-model='volume'` |
| 最低價 | 當日最低價格 | 使用 `c-model-dazzle` 屬性 |
| 前一日收盤價 | 昨日收盤價 | 使用 `c-model='previousClose'` |

#### 2. 瀏覽器配置 (BrowserConfig)

```python
browserConfig = BrowserConfig(
    headless=False,          # 非 Headless 模式，顯示瀏覽器視窗
    verbose=True,            # 啟用詳細日誌
    browser_mode="dedicated" # 專用瀏覽器模式
)
```

**配置說明**：
- **headless=False**: 顯示瀏覽器視窗，方便觀察爬蟲過程和除錯
- **verbose=True**: 輸出詳細的執行日誌
- **browser_mode="dedicated"**: 使用專用瀏覽器實例（每次啟動獨立瀏覽器）

#### 3. JavaScript 指令執行

```python
js_command = [
    "document.querySelector('.my-drawer-toggle-btn')?.click();"
]
```

**功能說明**：
- 在頁面載入後執行 JavaScript 指令
- 點擊特定按鈕（`.my-drawer-toggle-btn`）觸發頁面互動
- 使用可選鏈運算子 `?.` 避免元素不存在時報錯

#### 4. 爬蟲執行配置 (CrawlerRunConfig)

```python
config = CrawlerRunConfig(
    extraction_strategy=extraction_strategy,  # 使用自訂的擷取策略
    cache_mode=CacheMode.BYPASS,             # 繞過快取
    scan_full_page=True,                     # 掃描完整頁面
    js_code=js_command,                      # 執行 JavaScript 指令
    verbose=True                             # 啟用詳細日誌
)
```

**關鍵參數解析**：
- **scan_full_page=True**: 掃描整個頁面內容，確保所有動態載入的資料都被擷取
- **js_code**: 在頁面載入後執行的 JavaScript 指令陣列
- **cache_mode=CacheMode.BYPASS**: 繞過快取，確保取得最新即時資料

## 使用方式

### 1. 安裝相依套件

```bash
pip install crawl4ai
```

### 2. 執行程式

```bash
python main.py
```

**注意**：由於使用 `headless=False`，程式執行時會開啟瀏覽器視窗。

### 3. 程式輸出範例

```json
[
  {
    "日期時間": "2025/01/15 13:30:00",
    "股票號碼": "2330",
    "股票名稱": "台積電",
    "即時價格": "615.00",
    "漲跌": "+5.00",
    "漲跌百分比": "+0.82%",
    "開盤價": "610.00",
    "最高價": "617.00",
    "成交量(張)": "45,678",
    "最低價": "609.00",
    "前一日收盤價": "610.00"
  }
]
```

### 4. 修改股票代碼

若要爬取其他股票，修改 `main.py` 中的 URL：

```python
# 範例：爬取鴻海 (2317)
url = "https://www.wantgoo.com/stock/2317/technical-chart"

# 範例：爬取聯發科 (2454)
url = "https://www.wantgoo.com/stock/2454/technical-chart"
```

## 核心技術解析

### 1. 動態網頁爬蟲

**挑戰**：
- 玩股網使用 JavaScript 動態渲染內容
- 資料不在原始 HTML 中，需等待 JavaScript 執行後才會出現

**解決方案**：
```python
# 使用真實瀏覽器執行 JavaScript
browserConfig = BrowserConfig(headless=False)

# 掃描完整頁面，等待動態內容載入
config = CrawlerRunConfig(scan_full_page=True)
```

### 2. CSS 選擇器進階應用

本專案展示了多種 CSS 選擇器技巧：

#### 使用自訂屬性（Custom Attributes）
```python
"selector": "span.astock-code[c-model='id']"
```
- 目標網站使用自訂屬性 `c-model` 綁定資料
- 比傳統的 class/id 選擇器更穩定

#### 複雜屬性選擇器
```python
"selector": "span[c-model-dazzle='text:open,class:openUpDn']"
```

#### 層級選擇器
```python
"selector": "div.quotes-info #quotesUl span[c-model='volume']"
```

## 常見問題 (FAQ)

### Q1: 為什麼要使用 headless=False？

A: `headless=False` 會顯示瀏覽器視窗，有以下優點：

**優點**：
- 觀察爬蟲過程，方便除錯
- 確認 JavaScript 是否正確執行
- 檢查是否觸發反爬蟲機制

**生產環境建議**：
```python
browserConfig = BrowserConfig(
    headless=True,  # 改為 True
    verbose=False   # 關閉詳細日誌
)
```

### Q2: CSS 選擇器如何找到？

A: 使用瀏覽器開發者工具：

1. 開啟目標網頁
2. 按 F12 開啟開發者工具
3. 使用「元素選擇器」（Ctrl+Shift+C）點擊目標資料
4. 在 Elements 面板中查看 HTML 結構
5. 右鍵選擇「Copy → Copy selector」

### Q3: 為什麼擷取的資料是空的？

A: 可能的原因與解決方法：

**原因 1：資料尚未載入**
```python
# 增加等待時間
config = CrawlerRunConfig(
    wait_until="networkidle",  # 等待網路閒置
    page_timeout=30000         # 增加超時時間（毫秒）
)
```

**原因 2：選擇器錯誤**
- 檢查 CSS 選擇器是否正確
- 使用瀏覽器開發者工具驗證

### Q4: 如何爬取多支股票？

A: 建立股票代碼列表並批次爬取：

```python
async def crawl_multiple_stocks():
    stock_codes = ["2330", "2317", "2454", "2412", "2308"]

    for code in stock_codes:
        url = f"https://www.wantgoo.com/stock/{code}/technical-chart"
        # 執行爬蟲...
        await asyncio.sleep(2)  # 避免請求過於頻繁
```

## 學習重點

### 與專案 1 的主要差異

| 特性 | 專案 1（銀行匯率） | 專案 2（股票資訊） |
|-----|------------------|-------------------|
| **網頁類型** | 靜態網頁 | 動態網頁（JavaScript 渲染） |
| **技術難度** | ⭐⭐ 初級 | ⭐⭐⭐⭐ 中級 |
| **瀏覽器模式** | Headless（預設） | 非 Headless（顯示視窗） |
| **JavaScript** | 不需執行 | 需執行 JS 指令 |
| **頁面互動** | 無 | 有（點擊按鈕） |
| **選擇器複雜度** | 簡單 | 複雜（自訂屬性） |

### 核心學習概念

#### 1. 動態網頁 vs 靜態網頁

**靜態網頁**：
- HTML 內容在伺服器端生成
- 簡單的 HTTP 請求即可取得資料

**動態網頁**：
- 內容由 JavaScript 動態生成
- 需要執行 JavaScript 才能取得資料

#### 2. CSS 選擇器進階技巧

- 使用自訂屬性選擇器
- 組合多層級選擇器提升精確度

#### 3. JavaScript 指令執行

- 使用 `querySelector` 選擇元素
- 可選鏈運算子 `?.` 避免錯誤

## 相關資源

### 官方文件
- [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)
- [Crawl4AI 文件](https://docs.crawl4ai.com/)

### 相關專案
- [實際案例 1: 台灣銀行牌告匯率](../01_台灣銀行牌告匯率/) - 靜態網頁爬蟲入門
- [實際案例 4: 台灣即時股票資訊_tkinter](../03_股票批次爬取_GUI/) - 加入 GUI 介面

## 注意事項與免責聲明

1. **遵守使用條款**：使用前請閱讀目標網站的使用條款
2. **合理請求頻率**：避免過於頻繁的請求
3. **個人使用為主**：本專案僅供學習與個人使用
4. **投資風險**：股票資料僅供參考，不構成投資建議

## 版本歷史

- **v1.0** (2025-01): 初始版本
  - 支援台積電 (2330) 即時資料爬取
  - 實作 JavaScript 互動功能

---

**最後更新**: 2025-01-15  
**作者**: Robert Hsu  
**授權**: MIT License  
**學習難度**: ⭐⭐⭐⭐ 中級
