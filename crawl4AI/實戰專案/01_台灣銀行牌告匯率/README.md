# 台灣銀行牌告匯率爬蟲

## 專案簡介

這是一個使用 Crawl4AI 框架自動爬取台灣銀行牌告匯率的實戰專案。程式會定期從台灣銀行官網擷取最新的外幣匯率資訊，並儲存為 JSON 格式供後續使用。

**目標網站**: [台灣銀行牌告匯率](https://rate.bot.com.tw/xrt?Lang=zh-TW)

**主程式-main.py**:[main.py](./main.py)

## 功能特色

- ✅ 自動化擷取台灣銀行牌告匯率
- ✅ 支援多幣別（美金、日圓、港幣、英鎊等）
- ✅ 擷取完整匯率資訊（現金買入/賣出、即期買入/賣出）
- ✅ 每 10 分鐘自動執行一次
- ✅ 資料以時間戳記命名並儲存為 JSON 格式
- ✅ 完整的錯誤處理與重試機制
- ✅ 使用非同步方式提升效能

## 環境需求

### Python 版本
- Python 3.8 或以上（建議使用 3.10+）

### 相依套件
```bash
pip install crawl4ai
```

## 專案結構

```
1台灣銀行牌告匯率/
├── main.py              # 主程式
├── README.md            # 本說明文件
└── data/                # 資料儲存目錄（自動建立）
    └── 台幣匯率_YYYYMMDD_HHMMSS.json
```

## 程式說明

### 核心功能模組

#### 1. 資料擷取策略 (JsonCssExtractionStrategy)

程式使用 CSS 選擇器定義資料擷取的結構：

```python
schema = {
    "name": "台幣匯率",
    "baseSelector": "table[title='牌告匯率'] tr",  # 基礎選擇器：匯率表格的每一行
    "fields": [
        {
            "name": "幣名",
            "selector": "td[data-table='幣別'] div.visible-phone.print_hide",
            "type": "text"
        },
        {
            "name": "現金匯率_本行買入",
            "selector": '[data-table="本行現金買入"]',
            "type": "text"
        },
        {
            "name": "現金匯率_本行賣出",
            "selector": '[data-table="本行現金賣出"]',
            "type": "text"
        },
        {
            "name": "即期匯率_本行買入",
            "selector": '[data-table="本行即期買入"]',
            "type": "text"
        },
        {
            "name": "即期匯率_本行賣出",
            "selector": '[data-table="本行即期賣出"]',
            "type": "text"
        }
    ]
}
```

**欄位說明**：
- **幣名**: 外幣名稱（如：美金、日圓）
- **現金匯率_本行買入**: 銀行以現金買入該外幣的匯率
- **現金匯率_本行賣出**: 銀行以現金賣出該外幣的匯率
- **即期匯率_本行買入**: 銀行即期買入該外幣的匯率（通常用於大額交易）
- **即期匯率_本行賣出**: 銀行即期賣出該外幣的匯率

#### 2. 爬蟲配置 (CrawlerRunConfig)

```python
config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,           # 繞過快取，確保取得最新資料
    extraction_strategy=extraction_strategy # 使用自訂的擷取策略
)
```

#### 3. 非同步爬蟲執行

```python
async with AsyncWebCrawler(verbose=True) as crawler:
    result = await crawler.arun(
        url='https://rate.bot.com.tw/xrt?Lang=zh-TW',
        config=config
    )
```

**關鍵特點**：
- 使用 `async with` 確保資源正確釋放
- `verbose=True` 啟用詳細日誌，方便除錯
- 非同步執行提升效能

#### 4. 資料儲存機制

```python
# 建立基於時間的檔案名稱
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"台幣匯率_{timestamp}.json"

# 確保資料夾存在
os.makedirs("data", exist_ok=True)
filepath = os.path.join("data", filename)

# 儲存 JSON 檔案
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**檔案命名範例**: `台幣匯率_20250115_143020.json`

#### 5. 定時執行機制

```python
while True:
    try:
        await extract_crypto_prices()
        await asyncio.sleep(600)  # 等待 10 分鐘（600 秒）
    except KeyboardInterrupt:
        print("\n程式被使用者中斷")
        break
    except Exception as e:
        print(f"執行過程中發生錯誤: {e}")
        await asyncio.sleep(600)
```

**特色**：
- 無限迴圈持續執行
- 支援 Ctrl+C 優雅中斷
- 發生錯誤時自動重試

## 使用方式

### 1. 安裝相依套件

```bash
# 安裝 Crawl4AI
pip install crawl4ai
```

### 2. 執行程式

```bash
python main.py
```

### 3. 程式輸出範例

```
台幣匯率爬蟲程式啟動...
每10分鐘自動執行一次

=== 開始執行爬蟲 (2025-01-15 14:30:20) ===
Extracted 21 coin entries
資料已儲存至: data/台幣匯率_20250115_143020.json
[
  {
    "幣名": "美金 (USD)",
    "現金匯率_本行買入": "30.455",
    "現金匯率_本行賣出": "31.055",
    "即期匯率_本行買入": "30.755",
    "即期匯率_本行賣出": "30.855"
  },
  ...
]
=== 爬蟲執行完成 ===
等待10分鐘後再次執行...
```

### 4. 停止程式

按下 `Ctrl+C` 即可優雅地停止程式。

## 擷取資料格式

### JSON 輸出範例

```json
[
  {
    "幣名": "美金 (USD)",
    "現金匯率_本行買入": "30.455",
    "現金匯率_本行賣出": "31.055",
    "即期匯率_本行買入": "30.755",
    "即期匯率_本行賣出": "30.855"
  },
  {
    "幣名": "日圓 (JPY)",
    "現金匯率_本行買入": "0.2056",
    "現金匯率_本行賣出": "0.2136",
    "即期匯率_本行買入": "0.2096",
    "即期匯率_本行賣出": "0.2116"
  }
]
```

### 資料欄位說明

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| 幣名 | 外幣名稱及代碼 | "美金 (USD)" |
| 現金匯率_本行買入 | 銀行買入現金匯率 | "30.455" |
| 現金匯率_本行賣出 | 銀行賣出現金匯率 | "31.055" |
| 即期匯率_本行買入 | 銀行即期買入匯率 | "30.755" |
| 即期匯率_本行賣出 | 銀行即期賣出匯率 | "30.855" |

## 核心技術解析

### 1. JsonCssExtractionStrategy

這是 Crawl4AI 提供的結構化資料擷取策略：

**優點**：
- 使用 CSS 選擇器定義擷取規則
- 自動將網頁轉換為結構化 JSON
- 不需手動解析 HTML

**關鍵參數**：
- `baseSelector`: 定義資料的基礎單位（每一筆資料）
- `fields`: 定義要擷取的欄位及其選擇器
- `verbose`: 啟用詳細日誌

### 2. CacheMode.BYPASS

```python
cache_mode=CacheMode.BYPASS
```

**作用**: 繞過 Crawl4AI 的快取機制，確保每次都取得最新資料。

**重要性**: 對於即時性要求高的匯率資料，必須關閉快取。

### 3. 非同步程式設計 (asyncio)

**優點**：
- 單執行緒內實現並發
- 適合 I/O 密集型任務（如網路請求）
- 不會因等待網路回應而阻塞程式

**關鍵概念**：
```python
async def extract_crypto_prices():  # 定義非同步函數
    await crawler.arun(...)          # 等待非同步操作完成
    await asyncio.sleep(600)         # 非同步等待
```

### 4. 錯誤處理機制

程式包含三層錯誤處理：

```python
# 第1層：檢查爬蟲是否成功
if not result.success:
    print("Crawl failed:", result.error_message)
    return

# 第2層：捕捉使用者中斷
except KeyboardInterrupt:
    print("\n程式被使用者中斷")
    break

# 第3層：捕捉所有其他錯誤
except Exception as e:
    print(f"執行過程中發生錯誤: {e}")
    await asyncio.sleep(600)  # 錯誤後等待再重試
```

## 常見問題 (FAQ)

### Q1: 為什麼要每 10 分鐘執行一次？

A: 台灣銀行的牌告匯率更新頻率不高（通常每日或數小時更新），10 分鐘是一個平衡的間隔。您可以根據需求調整：

```python
await asyncio.sleep(600)  # 改為其他秒數
```

### Q2: 如何只執行一次而不持續運行？

A: 將 `main.py` 的主程式改為：

```python
if __name__ == "__main__":
    asyncio.run(extract_crypto_prices())  # 只執行一次
```

### Q3: 資料儲存太多怎麼辦？

A: 可以修改程式只保留最新資料，或改為覆寫同一檔案：

```python
filename = "台幣匯率_最新.json"  # 固定檔名，每次覆寫
```

### Q4: 如何擷取特定幣別？

A: 在取得資料後過濾：

```python
# 只保留美金和日圓
filtered_data = [item for item in data
                 if '美金' in item['幣名'] or '日圓' in item['幣名']]
```

### Q5: 爬蟲失敗怎麼辦？

A: 檢查以下幾點：
1. 網路連線是否正常
2. 目標網站是否變更結構
3. Crawl4AI 是否正確安裝
4. 查看 `verbose=True` 的詳細日誌

### Q6: 如何加入通知功能？

A: 可以整合 LINE Notify 或 Email：

```python
import requests

def send_line_notify(message):
    token = 'YOUR_LINE_NOTIFY_TOKEN'
    headers = {'Authorization': f'Bearer {token}'}
    data = {'message': message}
    requests.post('https://notify-api.line.me/api/notify',
                  headers=headers, data=data)

# 在擷取完成後呼叫
send_line_notify(f"匯率更新完成，共 {len(data)} 筆資料")
```

## 進階應用

### 1. 整合資料庫

將資料儲存到 SQLite 或 PostgreSQL：

```python
import sqlite3

def save_to_db(data):
    conn = sqlite3.connect('exchange_rates.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rates (
            timestamp TEXT,
            currency TEXT,
            cash_buy REAL,
            cash_sell REAL,
            spot_buy REAL,
            spot_sell REAL
        )
    ''')

    for item in data:
        cursor.execute('''
            INSERT INTO rates VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), item['幣名'], ...))

    conn.commit()
    conn.close()
```

### 2. 建立 API 服務

使用 FastAPI 提供匯率查詢 API：

```python
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/rates")
def get_latest_rates():
    # 讀取最新的 JSON 檔案
    with open('data/台幣匯率_最新.json', 'r') as f:
        return json.load(f)

@app.get("/rates/{currency}")
def get_currency_rate(currency: str):
    with open('data/台幣匯率_最新.json', 'r') as f:
        data = json.load(f)
        return [item for item in data if currency in item['幣名']]
```

### 3. 資料視覺化

使用 Matplotlib 繪製匯率走勢圖：

```python
import matplotlib.pyplot as plt
import pandas as pd

# 讀取多個 JSON 檔案，合併為 DataFrame
# 繪製美金匯率趨勢圖
```

### 4. 匯率提醒功能

當匯率達到設定值時發送通知：

```python
def check_alert(data, alert_rules):
    """
    alert_rules = {
        '美金': {'buy_below': 30.0, 'sell_above': 31.5}
    }
    """
    for item in data:
        for currency, rules in alert_rules.items():
            if currency in item['幣名']:
                buy_rate = float(item['現金匯率_本行買入'])
                if 'buy_below' in rules and buy_rate < rules['buy_below']:
                    send_alert(f"{currency}買入匯率低於{rules['buy_below']}")
```

## 學習重點

### 適合初學者的特點

1. **靜態網頁爬蟲**: 台灣銀行匯率表是典型的靜態表格，適合入門
2. **結構化資料**: 使用 CSS Schema 輕鬆定義擷取規則
3. **實用性高**: 真實的金融資料應用場景
4. **完整流程**: 包含擷取、儲存、定時執行、錯誤處理

### 核心概念

- ✅ JsonCssExtractionStrategy 的使用
- ✅ 非同步程式設計 (async/await)
- ✅ CSS 選擇器應用
- ✅ JSON 資料處理
- ✅ 定時任務實作
- ✅ 錯誤處理與重試機制

## 相關資源

### 官方文件
- [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)
- [Crawl4AI 文件](https://docs.crawl4ai.com/)
- [Python asyncio 教學](https://docs.python.org/zh-tw/3/library/asyncio.html)

### 相關專案
- [實際案例 2: 台灣即時股票資訊](../02_台灣即時股票資訊/)
- [實際案例 4: 台灣即時股票資訊_tkinter](../03_股票批次爬取_GUI/)

## 授權與免責聲明

本專案僅供教學與學習用途。使用本程式擷取資料時，請遵守以下原則：

1. 遵守台灣銀行網站的使用條款
2. 不要過於頻繁地請求（目前設定為 10 分鐘一次）
3. 擷取的資料僅供個人參考，不構成投資建議
4. 使用者應自行承擔使用本程式的所有風險

## 版本歷史

- **v1.0** (2025-01): 初始版本
  - 基本匯率擷取功能
  - 定時執行機制
  - JSON 儲存功能

## 貢獻與回饋

如有任何問題、建議或改進，歡迎提出 Issue 或 Pull Request。

---

**最後更新**: 2025-01-15
**作者**: Robert Hsu
**授權**: MIT License
