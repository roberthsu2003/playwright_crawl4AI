# Crawl4AI 快速入門指南

> 這是一份完整的 Crawl4AI 教學文件，從基礎到進階，幫助你快速掌握現代化的網頁爬蟲技術。

## 📋 目錄

- [1. 簡介](#1-簡介)
- [2. 快速開始](#2-快速開始)
- [3. 基本配置](#3-基本配置)
- [4. Markdown 輸出](#4-markdown-輸出)
- [5. 資料擷取策略](#5-資料擷取策略)
  - [5.1 手動定義 CSS Schema](#51-手動定義-css-schema)
  - [5.2 手動 Schema 實際案例](#52-手動-schema-實際案例)
  - [5.3 使用 LLM 自動產生 Schema](#53-使用-llm-自動產生-schema)
  - [5.4 使用 LLM 提示詞引導擷取](#54-使用-llm-提示詞引導擷取)

---

## 📚 重要參考資料

- [**官方 Quick Start 文件**](https://docs.crawl4ai.com/core/quickstart/)
- [**Crawl4AI v0.7.7 核心類別介紹**](./crawl4ai_entities.md) - 深入了解 `AsyncWebCrawler`、`BrowserConfig`、`CrawlerRunConfig` 等核心類別
- [**完整範例程式：manual_control_example.py**](./manual_control_example.py) - 三種資料擷取方式的完整實作

---

## 1. 簡介

### 什麼是 Crawl4AI？

Crawl4AI 是一個現代化的 Python 網頁爬蟲框架，建構於 Playwright 之上，提供以下核心功能：

- ✅ **非同步爬蟲** - 使用 `AsyncWebCrawler` 實現高效能並發爬取
- ✅ **智慧型配置** - 透過 `BrowserConfig` 和 `CrawlerRunConfig` 精細控制行為
- ✅ **自動轉換** - 內建 `MarkdownGenerator` 將 HTML 轉換為 Markdown
- ✅ **多種擷取策略** - 支援 CSS/XPath 選擇器、LLM 輔助擷取
- ✅ **AI 賦能** - 整合 LLM（Ollama、GPT-4、Claude、Gemini）進行智慧擷取

### 核心架構

```
┌─────────────────────────────────────────────────┐
│              AsyncWebCrawler                     │  ← 主要爬蟲引擎
├─────────────────────────────────────────────────┤
│  BrowserConfig      │  CrawlerRunConfig         │  ← 配置層
├─────────────────────────────────────────────────┤
│  Markdown Generator │  Extraction Strategy      │  ← 處理層
├─────────────────────────────────────────────────┤
│  JsonCssExtraction  │  LLMExtractionStrategy   │  ← 擷取策略
└─────────────────────────────────────────────────┘
```

### 學習目標

完成本教學後，你將能夠：

- 使用最小配置運行爬蟲
- 產生 Markdown 輸出並了解內容過濾器
- 掌握基於 CSS 的資料擷取策略
- 理解基於 LLM 的智慧擷取（開源和閉源模型）
- 處理透過 JavaScript 載入的動態內容

---

## 2. 快速開始

### 2.1 第一個爬蟲

最簡單的爬蟲範例，只需 3 行核心程式碼：

**參考資源：** [第1個爬蟲.ipynb](./lesson1_第1個爬蟲.ipynb)

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:300])  # 顯示前 300 字

if __name__ == '__main__':
    await main()  # Jupyter Notebook 環境
    # asyncio.run(main())  # 一般 Python 環境
```

**程式說明：**

1. `AsyncWebCrawler()` - 建立非同步爬蟲實例
2. `crawler.arun(url)` - 爬取指定 URL
3. `result.markdown` - 取得自動轉換的 Markdown 內容

### 2.2 執行結果

```
<!DOCTYPE html>
<html>
<head>
    <title>Example Domain</title>
</head>
<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples...</p>
</div>
</body>
</html>
```

---

## 3. 基本配置

Crawl4AI 提供兩個核心配置類別，讓你精細控制爬蟲行為：

### 3.1 配置架構

| 配置類別 | 用途 | 主要參數 |
|---------|------|---------|
| **BrowserConfig** | 控制瀏覽器行為 | headless, user_agent, javascript |
| **CrawlerRunConfig** | 控制爬取行為 | cache_mode, extraction_strategy, timeout |

**參考資源：** [簡單配置.ipynb](./lesson2_基本配置.ipynb)

### 3.2 完整配置範例

```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    # 1. 配置瀏覽器
    browser_config = BrowserConfig(
        headless=True,           # 無頭模式（不顯示瀏覽器視窗）
        verbose=False            # 關閉詳細日誌
    )

    # 2. 配置爬取行為
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS  # 繞過快取，每次重新抓取
    )

    # 3. 執行爬蟲
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url='https://example.com',
            config=run_config
        )
        print(result.markdown)

if __name__ == "__main__":
    await main()
```

### 3.3 快取模式 (CacheMode)

```python
# CacheMode 選項說明
CacheMode.BYPASS      # 完全繞過快取，每次都重新抓取
CacheMode.ENABLED     # 啟用快取，優先使用已快取的資料
CacheMode.READ_ONLY   # 只讀模式，只從快取讀取
CacheMode.WRITE_ONLY  # 只寫模式，只更新快取
```

**使用建議：**
- **開發/測試** → `CacheMode.BYPASS`（確保獲取最新資料）
- **生產環境** → `CacheMode.ENABLED`（提升效能、減少請求）
- **唯讀分析** → `CacheMode.READ_ONLY`（分析已快取資料）

---

## 4. Markdown 輸出

Crawl4AI 會自動將 HTML 轉換為 Markdown，並支援內容過濾器來優化輸出品質。

### 4.1 Markdown 輸出類型

| 屬性 | 說明 | 適用場景 |
|------|------|---------|
| `result.markdown` | 原始 Markdown（未過濾） | 需要完整內容 |
| `result.markdown.fit_markdown` | 已套用內容過濾器 | 需要高品質內容 |

**參考資源：** [使用內容過濾器.ipynb](./lesson3_使用內容過濾器.ipynb)

### 4.2 使用內容過濾器

```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# 建立內容過濾器
content_filter = PruningContentFilter(
    threshold=0.4,           # 過濾閾值（0.0-1.0）
    threshold_type="fixed"   # 固定閾值模式
)

# 建立 Markdown 產生器
md_generator = DefaultMarkdownGenerator(
    content_filter=content_filter
)

# 配置爬蟲
config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://news.ycombinator.com", config=config)

    print(f"原始 Markdown 長度: {len(result.markdown.raw_markdown)}")
    print(f"過濾後 Markdown 長度: {len(result.markdown.fit_markdown)}")
```

### 4.3 內容過濾器工作原理

`PruningContentFilter` 會分析以下特徵來評分內容重要性：

- 📊 **文字密度** - 文字與標籤的比例
- 📏 **文字長度** - 內容的實際長度
- 🏷️ **標籤類型** - HTML 元素的語義重要性
- 🔗 **連結密度** - 連結與文字的比例

---

## 5. 資料擷取策略

Crawl4AI 提供多種資料擷取策略，從完全手動到完全自動化，滿足不同場景需求。

### 📊 擷取策略總覽

| 策略 | 控制程度 | 精確度 | LLM 成本 | 速度 | 適用場景 |
|------|---------|--------|---------|------|---------|
| **手動 CSS Schema** | 🔴 極高 | 🔴 極高 | ⚪ 無 | 🔴 極快 | 生產環境、結構已知 |
| **LLM 產生 Schema** | 🟡 低 | 🟡 中 | 🟡 一次性 | 🟢 快 | 快速原型、探索性爬蟲 |
| **LLM 提示詞引導** | 🟢 中 | 🔴 高 | 🔴 每次 | 🟡 慢 | 非結構化內容、語義理解 |

---

## 5.1 手動定義 CSS Schema

最精確、最快速的擷取方式，完全掌控 CSS 選擇器。

**官方文件：** [擷取策略說明](https://docs.crawl4ai.com/extraction/no-llm-strategies/)

### 5.1.1 Schema 結構

```python
schema = {
    "name": "Schema 名稱",           # 用於識別此擷取規則
    "baseSelector": "CSS選擇器",     # 定義資料容器範圍
    "fields": [                      # 欄位定義陣列
        {
            "name": "欄位名稱",         # JSON 中的 key
            "selector": "CSS選擇器",    # 元素選擇器
            "type": "text|attribute",  # 擷取類型
            "attribute": "屬性名"       # type=attribute 時必須
        }
    ]
}
```

### 5.1.2 基礎範例

```python
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    # 定義 Schema
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",  # 找出所有 class="item" 的 div
        "fields": [
            {
                "name": "title",
                "selector": "h2",
                "type": "text"       # 提取文字內容
            },
            {
                "name": "link",
                "selector": "a",
                "type": "attribute",  # 提取屬性值
                "attribute": "href"   # 屬性名稱
            }
        ]
    }

    # 測試 HTML
    html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

    # 建立擷取策略
    strategy = JsonCssExtractionStrategy(schema)

    # 配置爬蟲
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    # 執行爬蟲
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"raw://{html}",
            config=config
        )

        data = json.loads(result.extracted_content)
        print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    await main()
```

**執行結果：**

```json
[
    {
        "title": "Item 1",
        "link": "https://example.com/item1"
    }
]
```

### 5.1.3 Schema 欄位類型

| type 值 | 說明 | 額外參數 | 範例 |
|---------|------|---------|------|
| `text` | 提取元素文字內容 | - | `<h2>Title</h2>` → `"Title"` |
| `attribute` | 提取元素屬性值 | `attribute` | `<a href="...">` → URL |
| `html` | 提取元素的 HTML | - | `<div><p>...</p></div>` → HTML 字串 |

---

## 5.2 手動 Schema 實際案例

透過實際範例深入理解手動 Schema 的應用。

**更多範例：** [手動方式產生 css_schema](./手動方式產生css_schema)

### 5.2.1 加密貨幣價格擷取

```python
import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_crypto_prices():
    # 模擬加密貨幣網頁
    html = """
    <html>
      <body>
        <div class='crypto-row'>
          <h2 class='coin-name'>Bitcoin</h2>
          <span class='coin-price'>$28,000</span>
        </div>
        <div class='crypto-row'>
          <h2 class='coin-name'>Ethereum</h2>
          <span class='coin-price'>$1,800</span>
        </div>
      </body>
    </html>
    """

    # 1. 定義 Schema
    schema = {
        "name": "Crypto Prices",
        "baseSelector": "div.crypto-row",  # 有 2 個元素，所以會抓到 2 筆
        "fields": [
            {
                "name": "coin_name",
                "selector": "h2.coin-name",
                "type": "text"
            },
            {
                "name": "price",
                "selector": "span.coin-price",
                "type": "text"
            }
        ]
    }

    # 2. 建立擷取策略
    strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # 3. 配置爬蟲
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    # 4. 執行爬蟲
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=f"raw://{html}",
            config=config
        )

        if not result.success:
            print(f"爬取失敗：{result.error_message}")
            return

        # 5. 解析資料
        data = json.loads(result.extracted_content)
        print(f"成功擷取 {len(data)} 筆加密貨幣資料")
        print(json.dumps(data, indent=2, ensure_ascii=False))

# 執行
await extract_crypto_prices()
```

**執行結果：**

```json
[
  {
    "coin_name": "Bitcoin",
    "price": "$28,000"
  },
  {
    "coin_name": "Ethereum",
    "price": "$1,800"
  }
]
```

### 5.2.2 關鍵要點

⚠️ **重要提醒：**

1. **必須指定 extraction_strategy**
   ```python
   config = CrawlerRunConfig(
       extraction_strategy=strategy  # 必須明確指定
   )
   ```
   否則 `result.extracted_content` 會是 `None`

2. **baseSelector 決定資料筆數**
   - `baseSelector` 匹配幾個元素，就會擷取幾筆資料
   - 每個 `field` 都在 `baseSelector` 範圍內進行相對搜尋

3. **CSS 選擇器相對性**
   - 所有 `field.selector` 都是相對於 `baseSelector` 的
   - 例如：`baseSelector="div.item"` + `selector="h2"` = 找出 `div.item` 內的 `h2`

---

## 5.3 使用 LLM 自動產生 Schema

當網頁結構複雜或你不熟悉 CSS 選擇器時，可以讓 LLM 自動分析 HTML 並產生 Schema。

**參考資源：** [lesson4_css_base_使用llm建立schema.ipynb](./lesson4_css_base_使用llm建立schema.ipynb)

### 📋 LLM 產生 Schema 的工作原理

```
┌─────────────┐
│ 提供 HTML   │  → 你提供一個 HTML 範例
└──────┬──────┘
       ↓
┌─────────────┐
│ LLM 分析    │  → LLM 分析結構、識別模式
└──────┬──────┘
       ↓
┌─────────────┐
│ 產生 Schema │  → 自動產生 CSS 選擇器
└──────┬──────┘
       ↓
┌─────────────┐
│ 重複使用    │  → 後續擷取無需再次呼叫 LLM（一次性成本）
└─────────────┘
```

### ⚖️ 三種 Schema 產生方式比較

| 方式 | 控制程度 | 精確度 | LLM 成本 | 適用場景 |
|------|---------|--------|---------|---------|
| **手動定義** | 🔴 高 | 🔴 高 | ⚪ 無 | 生產環境、結構已知 |
| **LLM 自動產生** | 🟡 低 | 🟡 中 | 🟢 一次性 | 快速原型、探索性爬蟲 |
| **LLM 提示詞引導** | 🟢 中 | 🔴 高 | 🔴 每次 | 複雜擷取、非結構化內容 |

---

### 5.3.1 使用本地模型（Ollama）產生 Schema

#### 優點

- ✅ 免費、無需 API 金鑰
- ✅ 資料隱私（在本機執行）
- ✅ 支援多種開源模型（Llama、Mistral、Qwen 等）

#### 前置需求

```bash
# 1. 安裝 Ollama（參考：https://ollama.ai）
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# 2. 下載模型
ollama pull llama3.2
```

#### 完整範例

```python
import asyncio
import json
from pprint import pprint
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import LLMConfig, AsyncWebCrawler, CacheMode, CrawlerRunConfig

async def main():
    # 步驟 1: 準備 HTML 範例（用於讓 LLM 學習結構）
    html = """
    <div class='item'>
        <h2>Item 1</h2>
        <a href='https://example.com/item1'>Link 1</a>
    </div>
    """

    # 步驟 2: 使用 Ollama 本地模型自動產生 Schema（一次性成本）
    schema = JsonCssExtractionStrategy.generate_schema(
        html,
        llm_config=LLMConfig(
            provider="ollama/llama3.2",  # 本地 Ollama 模型
            api_token=None               # 本地模型不需要 API 金鑰
        )
    )

    print("===== Llama3.2 自動產生的 Schema =========")
    pprint(schema)
    print("\n說明：此 Schema 由 LLM 自動分析 HTML 產生")
    print("      後續擷取可重複使用，無需再次呼叫 LLM\n")

    # 步驟 3: 使用產生的 Schema 建立擷取策略
    strategy = JsonCssExtractionStrategy(schema)

    # 步驟 4: 設定爬蟲配置
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy  # ⚠️ 必須指定
    )

    # 步驟 5: 執行爬蟲擷取資料
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"raw://{html}",
            config=config
        )

        print("========== 擷取結果 ==========")
        data = json.loads(result.extracted_content)
        pprint(data)

if __name__ == "__main__":
    await main()  # Jupyter Notebook
    # asyncio.run(main())  # 一般 Python 環境
```

#### 執行結果範例

```python
# LLM 自動產生的 Schema
{
    'name': 'Items',
    'baseSelector': 'div.item',
    'fields': [
        {'name': 'title', 'selector': 'h2', 'type': 'text'},
        {'name': 'link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'}
    ]
}

# 擷取結果
[
    {
        'title': 'Item 1',
        'link': 'https://example.com/item1'
    }
]
```

---

### 5.3.2 使用雲端 LLM 產生 Schema

#### 優點與缺點

| 優點 | 缺點 |
|------|------|
| ✅ 更強大的推理能力 | ❌ 需要 API 金鑰和付費 |
| ✅ 更準確的 Schema 產生 | ❌ 資料需上傳至雲端 |
| ✅ 支援複雜 HTML 結構 | ❌ 有使用次數/費用限制 |

#### 使用 Google Gemini

```python
import asyncio
import json
from pprint import pprint
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai import LLMConfig, AsyncWebCrawler, CacheMode, CrawlerRunConfig

async def main():
    html = """
    <html>
        <body>
            <div class='product'>
                <h2>Gaming Laptop</h2>
                <span class='price'>$999.99</span>
            </div>
        </body>
    </html>
    """

    # 使用 Gemini 產生 Schema
    schema = JsonCssExtractionStrategy.generate_schema(
        html,
        llm_config=LLMConfig(
            provider="gemini/gemini-2.0-flash-exp",
            api_token="YOUR_GEMINI_API_KEY"  # 替換為你的 API 金鑰
        )
    )

    print("====== Gemini 自動產生的 Schema ======")
    pprint(schema)

    # 使用產生的 Schema 進行擷取
    strategy = JsonCssExtractionStrategy(schema, verbose=True)
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=f"raw://{html}", config=config)
        data = json.loads(result.extracted_content)
        print("\n======= 擷取結果 ===========")
        pprint(data)

if __name__ == "__main__":
    await main()
```

#### 使用 OpenAI GPT

```python
# 只需更改 LLM 配置
schema = JsonCssExtractionStrategy.generate_schema(
    html,
    llm_config=LLMConfig(
        provider="openai/gpt-4o-mini",
        api_token="YOUR_OPENAI_API_KEY"
    )
)
```

#### 使用 Anthropic Claude

```python
# 只需更改 LLM 配置
schema = JsonCssExtractionStrategy.generate_schema(
    html,
    llm_config=LLMConfig(
        provider="anthropic/claude-3-5-sonnet-20241022",
        api_token="YOUR_ANTHROPIC_API_KEY"
    )
)
```

---

### 5.3.3 手動 Schema vs LLM 產生的比較

```python
# 方法 A: LLM 自動產生（快速但不可控）
schema_auto = JsonCssExtractionStrategy.generate_schema(
    html,
    llm_config=LLMConfig(provider="ollama/llama3.2", api_token=None)
)

# 方法 B: 手動定義（精確可控）
schema_manual = {
    'name': 'Product Details',
    'baseSelector': '.product',
    'fields': [
        {'name': 'title', 'selector': 'h2', 'type': 'text'},
        {'name': 'price', 'selector': '.price', 'type': 'text'}
    ]
}

# 兩者都可以用於建立擷取策略
strategy_auto = JsonCssExtractionStrategy(schema_auto)
strategy_manual = JsonCssExtractionStrategy(schema_manual)
```

---

### 5.3.4 完整實作範例

**查看完整範例：** [manual_control_example.py](./manual_control_example.py)

這個範例展示了三種控制 Schema 的方法：

1. ✅ LLM 自動產生（快速原型）
2. ✅ 手動定義 Schema（生產環境）
3. ✅ 使用自訂提示詞引導 LLM（複雜擷取）

---

### 🎯 使用建議

| 場景 | 推薦方式 | 原因 |
|------|---------|------|
| 🚀 快速原型開發 | LLM 自動產生 | 快速、自動化 |
| 🏭 生產環境 | 手動定義 Schema | 精確、快速、無 LLM 成本 |
| 🔬 複雜網頁探索 | LLM 自動產生 | 節省手動分析時間 |
| 📊 大規模爬蟲 | 手動定義 Schema | 避免重複 LLM 成本 |
| 🧩 非結構化內容 | LLMExtractionStrategy | 需要 AI 理解語義 |

---

### ⚠️ 重要注意事項

#### 1. Schema 可重複使用

產生一次後，儲存 Schema 並重複使用，避免每次都呼叫 LLM：

```python
# 第一次：產生並儲存 Schema
schema = JsonCssExtractionStrategy.generate_schema(html, llm_config=...)
with open('schema.json', 'w') as f:
    json.dump(schema, f)

# 後續使用：直接載入
with open('schema.json', 'r') as f:
    schema = json.load(f)
strategy = JsonCssExtractionStrategy(schema)
```

#### 2. 必須指定 extraction_strategy

```python
config = CrawlerRunConfig(
    extraction_strategy=strategy  # 必須明確指定
)
```

否則 `result.extracted_content` 會是 `None`

#### 3. 本地 vs 雲端 LLM

| 階段 | 推薦 LLM | 原因 |
|------|---------|------|
| 開發/測試 | Ollama | 免費、快速迭代 |
| 複雜任務 | 雲端 LLM | 更準確、更強大 |
| 生產環境 | 手動 Schema | 無 LLM 成本 |

#### 4. HTML 範例品質

提供**完整且具代表性**的 HTML 範例，LLM 才能產生準確的 Schema：

```python
# ❌ 不好：不完整的 HTML
html = "<div><h2>Title</h2></div>"

# ✅ 好：完整的結構
html = """
<div class='product'>
    <h2 class='title'>Gaming Laptop</h2>
    <span class='price'>$999.99</span>
    <a href='/product/123' class='link'>View</a>
</div>
"""
```

---

## 5.4 使用 LLM 提示詞引導擷取(目前測試效果不好)

前面的方法都是使用 `JsonCssExtractionStrategy`（基於 CSS 選擇器），但有時候網頁結構非常複雜、不規則，或者需要 AI 理解語義內容時，可以使用 `LLMExtractionStrategy`，讓 LLM **每次執行時**根據自訂提示詞來擷取資料。

### 📊 LLMExtractionStrategy vs JsonCssExtractionStrategy

| 特性 | JsonCssExtractionStrategy | LLMExtractionStrategy |
|------|--------------------------|----------------------|
| **擷取方式** | CSS 選擇器（結構化） | LLM 理解（語義化） |
| **LLM 成本** | 僅產生 Schema 時（一次性）或無 | **每次擷取都需要** |
| **速度** | 🔴 快（直接解析 DOM） | 🟡 慢（需要 LLM 推理） |
| **精確度** | 🔴 高（結構已知） | 🟡 中到高（依提示詞品質） |
| **適用場景** | 結構化、重複的資料 | 非結構化、語義理解 |
| **彈性** | 🟡 低（依賴 HTML 結構） | 🔴 高（理解內容語義） |

---

### 5.4.1 基本 LLM 提示詞擷取

使用 `LLMExtractionStrategy` 時，你需要提供清晰的 `instruction`（指令）告訴 LLM 要擷取什麼資料。

#### 程式碼範例

```python
import asyncio
import json
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def main():
    # 測試用 HTML（模擬電商網頁）
    html = """
    <html>
        <body>
            <div class='product-card'>
                <h2>電競筆電 - 高效能遊戲機</h2>
                <p>這款筆電配備最新的 RTX 4070 顯示卡，
                   搭配 Intel i9 處理器，適合專業遊戲玩家。</p>
                <div class='price-section'>
                    <span class='old-price'>原價 $1499.99</span>
                    <span class='new-price'>特價 $1299.99</span>
                </div>
                <a href='https://example.com/gaming-laptop'>查看詳情</a>
            </div>
            <div class='product-card'>
                <h2>無線滑鼠 - 人體工學設計</h2>
                <p>符合人體工學的無線滑鼠，電池續航力長達 3 個月。</p>
                <div class='price-section'>
                    <span class='new-price'>$29.99</span>
                </div>
                <a href='https://example.com/wireless-mouse'>查看詳情</a>
            </div>
        </body>
    </html>
    """

    # 🔑 關鍵：自訂 LLM 提示詞
    custom_instruction = """
    請從網頁中擷取所有產品資訊，並以 JSON 格式返回。

    要求：
    1. 提取每個產品的以下資訊：
       - 產品名稱（從標題中提取）
       - 產品描述（簡短描述）
       - 原價（如果有的話，沒有則為 null）
       - 特價（當前售價）
       - 連結

    2. 返回格式：
    {
        "products": [
            {
                "name": "產品名稱",
                "description": "產品描述",
                "original_price": "原價或 null",
                "current_price": "當前售價",
                "url": "產品連結"
            }
        ],
        "total_count": 產品數量
    }

    3. 價格請保留貨幣符號和金額
    4. 如果沒有原價，original_price 設為 null
    """

    # 建立 LLM 擷取策略
    strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(provider="ollama/gpt-oss:20b"),
        api_token=None,
        instruction=custom_instruction  # 自訂提示詞
    )

    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=f"raw://{html}", config=config)

        print("========== LLM 擷取結果 ==========")
        print(result.extracted_content)

        # 嘗試解析為 JSON
        try:
            data = json.loads(result.extracted_content)
            print("\n========== 解析後的資料 ==========")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("\n⚠️ LLM 返回的內容不是有效的 JSON")

if __name__ == "__main__":
    await main()
```

---

### 5.4.2 使用雲端 LLM 進行語義擷取

使用更強大的雲端 LLM（如 GPT-4、Claude、Gemini）可以獲得更準確的結果，特別是在處理複雜的語義理解任務時。

#### 使用 OpenAI GPT-4

```python
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

instruction = """
請分析這個網頁的產品評論，並提取以下資訊：

1. 產品的優點（至少 3 個）
2. 產品的缺點（如果有）
3. 整體評分（1-5 星）
4. 是否推薦購買（是/否）

請以 JSON 格式返回：
{
    "pros": ["優點1", "優點2", ...],
    "cons": ["缺點1", "缺點2", ...],
    "rating": 4.5,
    "recommended": true
}
"""

strategy = LLMExtractionStrategy(
    provider="openai/gpt-4o-mini",
    api_token="YOUR_OPENAI_API_KEY",
    instruction=instruction
)

config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    extraction_strategy=strategy
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com/product-review",
        config=config
    )
    print(result.extracted_content)
```

#### 使用 Anthropic Claude

```python
strategy = LLMExtractionStrategy(
    provider="anthropic/claude-3-5-sonnet-20241022",
    api_token="YOUR_ANTHROPIC_API_KEY",
    instruction="""
    請分析這篇文章的主要論點，並提取：
    1. 核心論述
    2. 支持證據
    3. 結論

    以結構化 JSON 返回。
    """
)
```

#### 使用 Google Gemini

```python
strategy = LLMExtractionStrategy(
    provider="gemini/gemini-2.0-flash-exp",
    api_token="YOUR_GEMINI_API_KEY",
    instruction="""
    這是一個多語言網頁，請提取所有語言版本的內容，
    並標註每個內容的語言。
    """
)
```

---

### 5.4.3 進階提示詞技巧

#### 技巧 1：提供明確的輸出格式

```python
instruction = """
請嚴格按照以下 JSON Schema 格式返回資料：

{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "in_stock": {"type": "boolean"}
    },
    "required": ["title", "price", "in_stock"]
}

範例輸出：
{
    "title": "商品名稱",
    "price": 99.99,
    "in_stock": true
}
"""
```

#### 技巧 2：提供少樣本範例（Few-shot Learning）

```python
instruction = """
請從網頁中提取產品資訊。以下是範例：

輸入 HTML：
<div><h2>筆電</h2><span>$999</span></div>

輸出 JSON：
{"name": "筆電", "price": 999}

現在請處理實際的網頁內容，使用相同的格式。
"""
```

#### 技巧 3：處理非結構化內容

```python
instruction = """
這是一個部落格文章，請提取：

1. 文章標題
2. 作者名稱
3. 發布日期（格式：YYYY-MM-DD）
4. 文章摘要（100 字以內）
5. 主要標籤/分類（陣列）

注意：
- 日期可能以各種格式出現，請統一轉換為 YYYY-MM-DD
- 如果找不到某個欄位，請設為 null
- 摘要請從文章前幾段提取關鍵資訊
"""
```

---

### 5.4.4 完整實戰範例：新聞文章擷取

```python
import asyncio
import json
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def extract_news_article():
    """使用 LLM 提示詞擷取新聞文章的結構化資訊"""

    html = """
    <html>
        <body>
            <article>
                <h1>台灣科技業迎來新突破：AI 晶片出貨量創新高</h1>
                <div class='meta'>
                    <span class='author'>記者：張小明</span>
                    <span class='date'>2024 年 3 月 15 日</span>
                    <span class='category'>科技</span>
                </div>
                <div class='content'>
                    <p>台灣半導體產業在 2024 年第一季度表現亮眼，
                       AI 相關晶片出貨量較去年同期成長 150%。</p>
                    <p>業界專家表示，這波成長主要受惠於全球 AI 應用的快速普及，
                       特別是在自動駕駛和智慧製造領域。</p>
                    <p>預計未來三年，台灣在全球 AI 晶片市場的佔有率
                       將從目前的 25% 提升至 35%。</p>
                </div>
                <div class='tags'>
                    <span>#AI</span>
                    <span>#半導體</span>
                    <span>#台灣</span>
                </div>
            </article>
        </body>
    </html>
    """

    instruction = """
    你是一個專業的新聞內容分析助手。請從網頁中提取新聞文章資訊。

    要求：
    1. 提取文章標題
    2. 提取作者姓名（只要姓名，不要「記者：」等前綴）
    3. 提取發布日期，並轉換為 YYYY-MM-DD 格式
    4. 提取文章分類/類別
    5. 提取所有標籤（移除 # 符號）
    6. 生成文章摘要（50-100 字，包含關鍵數據）
    7. 提取文章中提到的關鍵數據（數字、百分比等）

    返回格式（嚴格遵守此 JSON 結構）：
    {
        "title": "文章標題",
        "author": "作者姓名",
        "publish_date": "YYYY-MM-DD",
        "category": "分類",
        "tags": ["標籤1", "標籤2"],
        "summary": "文章摘要...",
        "key_data": [
            {"metric": "指標名稱", "value": "數值"}
        ]
    }

    重要：
    - 請只返回 JSON，不要包含任何其他文字說明
    - 確保 JSON 格式正確且可解析
    - 如果某個欄位找不到，請設為 null 或空陣列
    """

    strategy = LLMExtractionStrategy(
        provider="ollama/llama3.2",
        api_token=None,
        instruction=instruction
    )

    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    print("開始擷取新聞文章...")

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=f"raw://{html}", config=config)

        if result.success:
            print("\n✅ 擷取成功！\n")
            print("========== LLM 原始回應 ==========")
            print(result.extracted_content)

            try:
                data = json.loads(result.extracted_content)
                print("\n========== 結構化資料 ==========")
                print(json.dumps(data, indent=2, ensure_ascii=False))

                print("\n========== 擷取結果摘要 ==========")
                print(f"📰 標題：{data.get('title')}")
                print(f"✍️  作者：{data.get('author')}")
                print(f"📅 日期：{data.get('publish_date')}")
                print(f"🏷️  分類：{data.get('category')}")
                print(f"🔖 標籤：{', '.join(data.get('tags', []))}")
                print(f"📊 關鍵數據：")
                for item in data.get('key_data', []):
                    print(f"   - {item.get('metric')}: {item.get('value')}")

            except json.JSONDecodeError as e:
                print(f"\n❌ JSON 解析失敗：{e}")
                print("提示：LLM 可能返回了非 JSON 格式的內容")
        else:
            print(f"❌ 擷取失敗：{result.error_message}")

if __name__ == "__main__":
    await extract_news_article()
```

**預期輸出：**

```json
{
  "title": "台灣科技業迎來新突破：AI 晶片出貨量創新高",
  "author": "張小明",
  "publish_date": "2024-03-15",
  "category": "科技",
  "tags": ["AI", "半導體", "台灣"],
  "summary": "台灣半導體產業在2024年第一季度AI晶片出貨量成長150%，預計未來三年全球市場佔有率將從25%提升至35%。",
  "key_data": [
    {"metric": "AI晶片出貨量成長率", "value": "150%"},
    {"metric": "目前全球市佔率", "value": "25%"},
    {"metric": "預計三年後市佔率", "value": "35%"}
  ]
}
```

---

### 5.4.5 LLMExtractionStrategy 的優缺點總結

#### ✅ 優點

1. **語義理解能力強**
   - 可以理解內容的含義，而非僅依賴 HTML 結構
   - 適合處理非結構化或結構變化的網頁

2. **高度彈性**
   - 通過改變提示詞即可調整擷取邏輯
   - 不需要分析 HTML 結構和編寫 CSS 選擇器

3. **處理複雜場景**
   - 可以進行內容摘要、分類、情感分析
   - 支援多語言內容處理

4. **容錯性好**
   - HTML 結構改變時，只要內容語義不變，仍可正常擷取

#### ❌ 缺點

1. **成本高**
   - 每次擷取都需要呼叫 LLM
   - 雲端 LLM 需要支付 API 費用

2. **速度慢**
   - LLM 推理需要時間（通常數秒）
   - 不適合大規模、高頻率爬蟲

3. **結果不確定**
   - LLM 可能返回不符合預期格式的內容
   - 需要處理 JSON 解析錯誤

4. **提示詞工程複雜**
   - 需要精心設計提示詞才能獲得準確結果
   - 可能需要多次調整和測試

---

### 🎯 何時使用 LLMExtractionStrategy？

| 場景 | 是否推薦 | 原因 |
|------|---------|------|
| 結構化商品列表 | ❌ | 用 JsonCssExtractionStrategy 更快更便宜 |
| 新聞文章摘要 | ✅ | 需要語義理解和內容總結 |
| 複雜的評論分析 | ✅ | 需要情感分析和觀點提取 |
| 大規模資料爬蟲 | ❌ | 成本高、速度慢 |
| HTML 結構經常變動 | ✅ | 容錯性好，不依賴固定結構 |
| 多語言內容處理 | ✅ | LLM 擅長跨語言理解 |
| 需要內容分類/標註 | ✅ | LLM 可以進行語義分類 |

---

### 💡 最佳實踐建議

#### 1. 混合使用策略

```python
# 結構化資料 → JsonCssExtractionStrategy
# 非結構化內容 → LLMExtractionStrategy

# 範例：同一個網站使用不同策略
# 商品列表：使用 CSS 選擇器（快速、便宜）
product_strategy = JsonCssExtractionStrategy(product_schema)

# 商品評論：使用 LLM 提示詞（語義理解）
review_strategy = LLMExtractionStrategy(
    provider="ollama/llama3.2",
    instruction="分析產品評論，提取優缺點和評分"
)
```

#### 2. 快取 LLM 結果

```python
config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,  # 啟用快取
    extraction_strategy=strategy
)
```

#### 3. 提示詞版本控制

```python
# 將提示詞儲存為單獨的檔案或變數
INSTRUCTION_V1 = """
請提取產品名稱和價格。
"""

INSTRUCTION_V2 = """
請提取產品名稱、價格、描述和評分。
如果沒有評分，請設為 null。
"""  # 改進版本

# 使用時
strategy = LLMExtractionStrategy(
    provider="ollama/llama3.2",
    instruction=INSTRUCTION_V2
)
```

#### 4. 錯誤處理

```python
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url=url, config=config)

    try:
        data = json.loads(result.extracted_content)
    except json.JSONDecodeError:
        # 方案 A：使用正則表達式提取 JSON
        import re
        json_match = re.search(r'\{.*\}', result.extracted_content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
        else:
            # 方案 B：回退到基本擷取策略
            print("⚠️ LLM 返回格式錯誤，使用備用方案")
            # 使用 JsonCssExtractionStrategy 重試
```

---

## 📚 總結與下一步

### 快速回顧

| 章節 | 重點 | 適用場景 |
|------|------|---------|
| **快速開始** | 最小配置運行爬蟲 | 初學者入門 |
| **基本配置** | BrowserConfig + CrawlerRunConfig | 所有場景 |
| **Markdown 輸出** | 內容過濾器 | 需要高品質內容 |
| **手動 CSS Schema** | 精確控制 | 生產環境 |
| **LLM 產生 Schema** | 自動化 | 快速原型 |
| **LLM 提示詞引導** | 語義理解 | 非結構化內容 |

### 擷取策略決策樹

```
需要擷取資料？
    │
    ├─ 結構化、重複的資料？
    │   └─ 是 → 使用 JsonCssExtractionStrategy
    │           └─ 熟悉 CSS？
    │               ├─ 是 → 手動定義 Schema
    │               └─ 否 → LLM 產生 Schema（一次性）
    │
    └─ 非結構化、語義理解？
        └─ 是 → 使用 LLMExtractionStrategy
                └─ 每次擷取都需要 LLM
```

### 推薦學習路徑

1. ✅ **階段 1：基礎**（已完成）
   - 快速開始
   - 基本配置
   - Markdown 輸出

2. 🎯 **階段 2：進階**（建議繼續）
   - 動態網頁爬取（JavaScript 渲染）
   - 多頁面並發爬取
   - 錯誤處理與重試機制

3. 🚀 **階段 3：實戰**（推薦練習）
   - [台灣銀行匯率爬蟲](../../實戰專案/01_台灣銀行牌告匯率/)
   - [台灣即時股票資訊](../../實戰專案/02_台灣即時股票資訊/)
   - [股票資訊 GUI 應用](../../實戰專案/03_股票批次爬取_GUI/)

### 相關資源

- 📖 [官方文件](https://docs.crawl4ai.com/)
- 💻 [GitHub Repository](https://github.com/unclecode/crawl4ai)
- 🎓 [完整教學專案](../../README.md)
- 🔧 [實際案例集](../../實戰專案/)

---

## 📞 支援與回饋

如果你在學習過程中遇到問題：

1. **查閱官方文件** - [docs.crawl4ai.com](https://docs.crawl4ai.com/)
2. **參考實際案例** - 本專案的 `實際案例/` 資料夾
3. **查看完整範例** - [manual_control_example.py](./manual_control_example.py)

---

**祝你學習愉快！Happy Crawling! 🚀**