"""
範例：比較 LLM 自動判斷 vs 手動控制提示詞

展示三種方式：
1. LLM 自動生成 Schema
2. 完全手動定義 Schema
3. 使用自訂提示詞引導 LLM
"""

from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai import LLMConfig, AsyncWebCrawler, CrawlerRunConfig, CacheMode
import json
import asyncio
from pprint import pprint

# 測試用 HTML
test_html = """
<div class='product-card'>
    <h2 class='product-title'>電競筆電</h2>
    <span class='product-price'>$1299.99</span>
    <p class='product-desc'>高效能遊戲筆電</p>
    <a href='https://example.com/laptop' class='product-link'>查看詳情</a>
</div>
<div class='product-card'>
    <h2 class='product-title'>無線滑鼠</h2>
    <span class='product-price'>$29.99</span>
    <p class='product-desc'>人體工學設計</p>
    <a href='https://example.com/mouse' class='product-link'>查看詳情</a>
</div>
"""


async def method1_llm_auto():
    """方法一：LLM 自動生成 Schema"""
    print("\n" + "="*60)
    print("方法一：LLM 自動生成 Schema")
    print("="*60)

    # LLM 自動分析 HTML 並生成 Schema
    schema = JsonCssExtractionStrategy.generate_schema(
        test_html,
        llm_config=LLMConfig(
            provider="ollama/llama3.2",
            api_token=None
        )
    )

    print("\n[LLM 生成的 Schema]")
    pprint(schema)

    strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"raw://{test_html}",
            config=config
        )

        print("\n[擷取結果]")
        data = json.loads(result.extracted_content)
        pprint(data)


async def method2_manual_schema():
    """方法二：完全手動定義 Schema（不使用 LLM）"""
    print("\n" + "="*60)
    print("方法二：手動定義 Schema（不使用 LLM）")
    print("="*60)

    # 手動定義精確的 Schema
    manual_schema = {
        "name": "產品列表",
        "baseSelector": "div.product-card",
        "fields": [
            {
                "name": "產品名稱",
                "selector": "h2.product-title",
                "type": "text"
            },
            {
                "name": "價格",
                "selector": "span.product-price",
                "type": "text"
            },
            {
                "name": "描述",
                "selector": "p.product-desc",
                "type": "text"
            },
            {
                "name": "連結",
                "selector": "a.product-link",
                "type": "attribute",
                "attribute": "href"
            }
        ]
    }

    print("\n[手動定義的 Schema]")
    pprint(manual_schema)

    strategy = JsonCssExtractionStrategy(manual_schema)
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"raw://{test_html}",
            config=config
        )

        print("\n[擷取結果]")
        data = json.loads(result.extracted_content)
        pprint(data)


async def method3_custom_instruction():
    """方法三：使用自訂提示詞引導 LLM"""
    print("\n" + "="*60)
    print("方法三：使用自訂提示詞引導 LLM")
    print("="*60)

    # 自訂詳細的提示詞
    custom_instruction = """
    請從網頁中擷取所有產品資訊，並按照以下格式返回：

    要求：
    1. 只擷取 class 為 'product-card' 的 div 元素
    2. 對每個產品，提取以下資訊：
       - 產品名稱（h2.product-title 的文字）
       - 價格（span.product-price 的文字，保留貨幣符號）
       - 描述（p.product-desc 的文字）
       - 連結（a.product-link 的 href 屬性）

    返回格式（JSON）：
    {
        "products": [
            {
                "name": "...",
                "price": "...",
                "description": "...",
                "url": "..."
            }
        ],
        "total_count": 數字
    }

    注意：請確保價格包含完整的貨幣符號和金額。
    """

    print("\n[自訂提示詞]")
    print(custom_instruction)

    strategy = LLMExtractionStrategy(
        provider="ollama/llama3.2",
        api_token=None,
        instruction=custom_instruction
    )

    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=f"raw://{test_html}",
            config=config
        )

        print("\n[擷取結果]")
        print(result.extracted_content)


async def main():
    """執行所有方法並比較結果"""
    print("\n" + "🔍 " + "="*58 + " 🔍")
    print("    LLM 資料擷取控制方法比較")
    print("🔍 " + "="*58 + " 🔍")

    try:
        # 方法一：LLM 自動判斷
        await method1_llm_auto()

        # 方法二：手動控制 Schema
        await method2_manual_schema()

        # 方法三：自訂提示詞
        await method3_custom_instruction()

    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
        print("\n💡 提示：")
        print("   1. 確保已安裝 Ollama 並下載 llama3.2 模型")
        print("   2. 執行：ollama pull llama3.2")
        print("   3. 確認 Ollama 服務正在運行")

    print("\n" + "="*60)
    print("比較總結")
    print("="*60)
    print("""
    方法一（LLM 自動）：
    優點：快速、自動化、適合探索性爬蟲
    缺點：不可預測、可能不精確、需要 LLM 成本

    方法二（手動 Schema）：
    優點：精確可控、快速執行、無 LLM 成本
    缺點：需要手動分析 HTML、維護成本高

    方法三（自訂提示詞）：
    優點：靈活、可引導 LLM 行為、適合複雜擷取
    缺點：需要精心設計提示詞、仍需 LLM 成本

    建議使用場景：
    - 原型開發/探索 → 方法一
    - 生產環境/大量爬蟲 → 方法二
    - 複雜/非結構化內容 → 方法三
    """)


if __name__ == "__main__":
    asyncio.run(main())