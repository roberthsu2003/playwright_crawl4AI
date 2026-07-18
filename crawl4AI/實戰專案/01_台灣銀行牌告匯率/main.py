#使用台灣銀行牌告匯率
#網址:https://rate.bot.com.tw/xrt?Lang=zh-TW

import asyncio
import json

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_exchange_rates() -> list[dict]:
#1. 定義一個簡單的extraction schema

    schema = {
        "name":"台幣匯率",
        "baseSelector":"table[title='牌告匯率'] tr",
        "fields":[
            {
                "name":"幣名",
                "selector":"td[data-table='幣別'] div.visible-phone.print_hide",
                "type":"text"
            },
            {
                "name":"現金匯率_本行買入",
                "selector":'[data-table="本行現金買入"]',
                "type":"text"
            },
            {
                "name":"現金匯率_本行賣出",
                "selector":'[data-table="本行現金賣出"]',
                "type":"text"
            },
            {
                "name":"即期匯率_本行買入",
                "selector":'[data-table="本行即期買入"]',
                "type":"text"
            },
            {
                "name":"即期匯率_本行賣出",
                "selector":'[data-table="本行即期賣出"]',
                "type":"text"
            }
        ]
    }
    
    #2. 建立extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True) #Enables verbose logging for debugging purposes.

    #3. 設定爬蟲配置
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=extraction_strategy
    )

    async with AsyncWebCrawler(verbose=True) as crawler:
        #4. 執行爬蟲和提取任務
        raw_url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
        result = await crawler.arun(
            url=raw_url,
            config=config
        )

        if not result.success:
            print("Crawl failed:", result.error_message)
            return []
        
        # 5. 解析被提取的json資料
        data = json.loads(result.extracted_content)
        print(f"Extracted {len(data)} coin entries")
        
        # 6. 課堂核心只驗證與顯示資料；本機儲存由 AI 賦能階段加入
        if data:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print("目前只顯示資料；SQLite 歷史儲存將在 AI 賦能階段加入。")
            return data
        else:
            print("No Data found")
            return []

async def main():
    """主程式：執行一次，讓學生專注於爬取與結構化。"""
    print("台幣匯率爬蟲程式啟動...")
    await extract_exchange_rates()
    print("=== 爬蟲執行完成 ===")

if __name__ == "__main__":
    asyncio.run(main())
