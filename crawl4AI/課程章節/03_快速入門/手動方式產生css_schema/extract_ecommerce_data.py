import json
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

# 教學案例：模擬新聞網站HTML結構
news_html = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>台灣新聞網 - 最新消息</title>
    <style>
        .news-section { border: 2px solid #333; padding: 20px; margin: 20px 0; }
        .section-title { color: #d32f2f; font-size: 24px; border-bottom: 3px solid #d32f2f; }
        .article { border: 1px solid #ddd; padding: 15px; margin: 15px 0; background: #f8f9fa; }
        .article-title { color: #1976d2; font-size: 18px; font-weight: bold; }
        .article-meta { background: #e3f2fd; padding: 8px; margin: 8px 0; }
        .article-tags { margin: 10px 0; }
        .tag { background: #4caf50; color: white; padding: 4px 8px; margin: 2px; border-radius: 12px; }
        .comment { border-top: 1px solid #eee; padding: 10px 0; margin: 5px 0; }
        .social-links { background: #fff3e0; padding: 10px; margin: 10px 0; }
    </style>
</head>
<body>
    <!-- 第一個新聞分類：科技新聞 -->
    <div class="news-section" data-section-id="tech">
        <h2 class="section-title">科技新聞</h2>
        <div class="section-description">最新科技動態與創新趨勢</div>
        
        <article class="article">
            <h3 class="article-title">AI人工智慧發展突破新里程碑</h3>
            <div class="article-meta">
                <span class="author">記者：王小明</span>
                <span class="date">2024-01-15</span>
                <span class="category">人工智慧</span>
            </div>
            <p class="article-content">台灣科技公司在AI領域取得重大突破，新開發的語言模型在多項測試中表現優異...</p>
            
            <!-- type: list 範例 - 文章標籤 -->
            <div class="article-tags">
                <span class="tag">人工智慧</span>
                <span class="tag">機器學習</span>
                <span class="tag">深度學習</span>
                <span class="tag">自然語言處理</span>
            </div>
            
            <!-- type: nested_list 範例 - 讀者評論 -->
            <div class="comments-section">
                <div class="comment">
                    <span class="commenter">張三</span>
                    <span class="comment-time">2024-01-15 14:30</span>
                    <p class="comment-text">這個發展真的很令人興奮！台灣在AI領域越來越強了</p>
                    <span class="comment-likes">👍 25</span>
                </div>
                <div class="comment">
                    <span class="commenter">李四</span>
                    <span class="comment-time">2024-01-15 15:45</span>
                    <p class="comment-text">希望能夠實際應用到生活中，改善我們的日常體驗</p>
                    <span class="comment-likes">👍 18</span>
                </div>
                <div class="comment">
                    <span class="commenter">陳五</span>
                    <span class="comment-time">2024-01-15 16:20</span>
                    <p class="comment-text">技術發展很快，但也要注意倫理問題</p>
                    <span class="comment-likes">👍 12</span>
                </div>
            </div>
            
            <!-- type: nested 範例 - 社群媒體連結 -->
            <div class="social-links">
                <div class="facebook-data">
                    <span class="platform">Facebook</span>
                    <span class="shares">分享: 156</span>
                    <span class="likes">按讚: 423</span>
                </div>
                <div class="twitter-data">
                    <span class="platform">Twitter</span>
                    <span class="shares">轉推: 89</span>
                    <span class="likes">喜歡: 234</span>
                </div>
            </div>
        </article>
        
        <article class="article">
            <h3 class="article-title">5G網路建設進度超前達標</h3>
            <div class="article-meta">
                <span class="author">記者：林小華</span>
                <span class="date">2024-01-14</span>
                <span class="category">通訊網路</span>
            </div>
            <p class="article-content">電信業者宣布5G基地台建設進度超前，預計今年底覆蓋率將達到95%...</p>
            
            <div class="article-tags">
                <span class="tag">5G</span>
                <span class="tag">電信</span>
                <span class="tag">基礎建設</span>
            </div>
            
            <div class="comments-section">
                <div class="comment">
                    <span class="commenter">劉六</span>
                    <span class="comment-time">2024-01-14 10:15</span>
                    <p class="comment-text">終於！期待已久的5G網路速度</p>
                    <span class="comment-likes">👍 67</span>
                </div>
                <div class="comment">
                    <span class="commenter">吳七</span>
                    <span class="comment-time">2024-01-14 11:30</span>
                    <p class="comment-text">希望資費也能夠更親民一些</p>
                    <span class="comment-likes">👍 45</span>
                </div>
            </div>
            
            <div class="social-links">
                <div class="facebook-data">
                    <span class="platform">Facebook</span>
                    <span class="shares">分享: 89</span>
                    <span class="likes">按讚: 267</span>
                </div>
                <div class="twitter-data">
                    <span class="platform">Twitter</span>
                    <span class="shares">轉推: 45</span>
                    <span class="likes">喜歡: 123</span>
                </div>
            </div>
        </article>
    </div>
    
    <!-- 第二個新聞分類：財經新聞 -->
    <div class="news-section" data-section-id="finance">
        <h2 class="section-title">財經新聞</h2>
        <div class="section-description">股市動態與經濟分析</div>
        
        <article class="article">
            <h3 class="article-title">台股創新高 外資持續看好</h3>
            <div class="article-meta">
                <span class="author">記者：黃大明</span>
                <span class="date">2024-01-15</span>
                <span class="category">股市</span>
            </div>
            <p class="article-content">台灣股市今日再創歷史新高，外資持續買超，市場信心十足...</p>
            
            <div class="article-tags">
                <span class="tag">台股</span>
                <span class="tag">外資</span>
                <span class="tag">投資</span>
                <span class="tag">經濟成長</span>
            </div>
            
            <div class="comments-section">
                <div class="comment">
                    <span class="commenter">投資達人</span>
                    <span class="comment-time">2024-01-15 09:30</span>
                    <p class="comment-text">長期投資還是王道，不要被短期波動影響</p>
                    <span class="comment-likes">👍 156</span>
                </div>
                <div class="comment">
                    <span class="commenter">理財新手</span>
                    <span class="comment-time">2024-01-15 10:45</span>
                    <p class="comment-text">請問現在進場還來得及嗎？</p>
                    <span class="comment-likes">👍 23</span>
                </div>
            </div>
            
            <div class="social-links">
                <div class="facebook-data">
                    <span class="platform">Facebook</span>
                    <span class="shares">分享: 234</span>
                    <span class="likes">按讚: 567</span>
                </div>
                <div class="twitter-data">
                    <span class="platform">Twitter</span>
                    <span class="shares">轉推: 123</span>
                    <span class="likes">喜歡: 345</span>
                </div>
            </div>
        </article>
    </div>
</body>
</html>
"""

# 教學重點：展示三種不同的提取類型
news_extraction_schema = {
    "name": "Taiwan News Website",
    "baseSelector": "div.news-section",  # 每個新聞分類作為基礎選擇器
    "fields": [
        # 基本文字提取
        {
            "name": "section_title",
            "selector": "h2.section-title",
            "type": "text"
        },
        {
            "name": "section_description", 
            "selector": "div.section-description",
            "type": "text"
        },
        {
            "name": "section_id",
            "selector": "",  # 空選擇器表示選擇當前元素
            "type": "attribute",
            "attribute": "data-section-id"
        },
        
        # type: nested_list - 文章列表（每個分類下的多篇文章）
        {
            "name": "articles",
            "selector": "article.article",
            "type": "nested_list",
            "fields": [
                {"name": "title", "selector": "h3.article-title", "type": "text"},
                {"name": "content", "selector": "p.article-content", "type": "text"},
                
                # type: nested - 文章詳細資訊（作為一個物件）
                {
                    "name": "meta_info",
                    "selector": "div.article-meta",
                    "type": "nested",
                    "fields": [
                        {"name": "author", "selector": "span.author", "type": "text"},
                        {"name": "date", "selector": "span.date", "type": "text"},
                        {"name": "category", "selector": "span.category", "type": "text"}
                    ]
                },
                
                # type: list - 標籤列表（簡單的文字列表）
                {
                    "name": "tags",
                    "selector": "div.article-tags span.tag",
                    "type": "list",
                    "fields": [{"name": "tag", "type": "text"}]
                },
                
                # type: nested_list - 評論列表（複雜的物件列表）
                {
                    "name": "comments",
                    "selector": "div.comments-section div.comment",
                    "type": "nested_list",
                    "fields": [
                        {"name": "commenter", "selector": "span.commenter", "type": "text"},
                        {"name": "time", "selector": "span.comment-time", "type": "text"},
                        {"name": "text", "selector": "p.comment-text", "type": "text"},
                        {"name": "likes", "selector": "span.comment-likes", "type": "text"}
                    ]
                },
                
                # type: nested - 社群媒體資訊（作為一個複合物件）
                {
                    "name": "social_media",
                    "selector": "div.social-links",
                    "type": "nested",
                    "fields": [
                        {
                            "name": "facebook",
                            "selector": "div.facebook-data",
                            "type": "nested",
                            "fields": [
                                {"name": "platform", "selector": "span.platform", "type": "text"},
                                {"name": "shares", "selector": "span.shares", "type": "text"},
                                {"name": "likes", "selector": "span.likes", "type": "text"}
                            ]
                        },
                        {
                            "name": "twitter", 
                            "selector": "div.twitter-data",
                            "type": "nested",
                            "fields": [
                                {"name": "platform", "selector": "span.platform", "type": "text"},
                                {"name": "shares", "selector": "span.shares", "type": "text"},
                                {"name": "likes", "selector": "span.likes", "type": "text"}
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

async def tutorial_extraction():
    """教學用的新聞網站資料提取"""
    print("🎓 crawl4ai 教學案例：新聞網站資料提取")
    print("=" * 60)
    print("本案例將展示三種重要的提取類型：")
    print("1. type: 'list' - 簡單的文字列表（如：標籤）")
    print("2. type: 'nested_list' - 複雜物件的列表（如：評論、文章）")
    print("3. type: 'nested' - 巢狀物件結構（如：作者資訊、社群媒體資料）")
    print("=" * 60)
    
    try:
        # 建立提取策略
        strategy = JsonCssExtractionStrategy(news_extraction_schema, verbose=True)
        
        # 設定爬蟲配置
        config = CrawlerRunConfig(
            word_count_threshold=1,
            user_agent="Mozilla/5.0 (compatible; NewsBot/1.0)",
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=strategy
        )
        
        # 執行爬取
        async with AsyncWebCrawler() as crawler:
            print("\n🔍 開始提取資料...")
            result = await crawler.arun(
                url=f"raw://{news_html}",
                config=config
            )
            
            if result.success and result.extracted_content:
                print("✅ 提取成功！")
                
                # 解析JSON資料
                extracted_data = json.loads(result.extracted_content)
                
                print("\n" + "="*60)
                print("📊 提取結果分析")
                print("="*60)
                
                # 顯示完整的提取結果
                print(json.dumps(extracted_data, indent=2, ensure_ascii=False))
                
                print("\n" + "="*60)
                print("📈 資料統計")  
                print("="*60)
                
                # 統計分析
                total_sections = len(extracted_data)
                print(f"📰 新聞分類總數: {total_sections}")
                
                for i, section in enumerate(extracted_data, 1):
                    section_title = section.get('section_title', '未知分類')
                    articles = section.get('articles', [])
                    article_count = len(articles)
                    
                    print(f"\n📋 分類 {i}: {section_title}")
                    print(f"   📄 文章數量: {article_count}")
                    
                    # 統計每篇文章的詳細資訊
                    for j, article in enumerate(articles, 1):
                        title = article.get('title', '無標題')
                        tags = article.get('tags', [])
                        comments = article.get('comments', [])
                        
                        print(f"   📝 文章 {j}: {title}")
                        print(f"      🏷️  標籤數量: {len(tags)} ({[tag.get('tag', '') for tag in tags]})")
                        print(f"      💬 評論數量: {len(comments)}")
                        
                        # 展示社群媒體資料結構
                        social = article.get('social_media', {})
                        if social:
                            fb_likes = social.get('facebook', {}).get('likes', '0')
                            tw_likes = social.get('twitter', {}).get('likes', '0')
                            print(f"      📱 社群互動: FB({fb_likes}) / Twitter({tw_likes})")
                
                print("\n" + "="*60)
                print("🎯 教學重點說明")
                print("="*60)
                print("1. type: 'list' 用法：")
                print("   - 提取標籤: div.article-tags span.tag")
                print("   - 結果: [{'tag': '人工智慧'}, {'tag': '機器學習'}, ...]")
                print("   - 適用: 簡單的文字列表")
                
                print("\n2. type: 'nested_list' 用法：")
                print("   - 提取評論: div.comments-section div.comment") 
                print("   - 結果: [{'commenter': '張三', 'text': '...', 'likes': '25'}, ...]")
                print("   - 適用: 複雜物件的重複列表")
                
                print("\n3. type: 'nested' 用法：")
                print("   - 提取作者資訊: div.article-meta")
                print("   - 結果: {'author': '記者：王小明', 'date': '2024-01-15', ...}")
                print("   - 適用: 單一複合物件結構")
                
            else:
                print("❌ 提取失敗")
                print(f"錯誤訊息: {result.error_message}")
                
    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

async def real_website_example():
    """真實網站爬取範例（以台灣新聞網站為例）"""
    print("\n🌐 真實網站爬取範例")
    print("=" * 40)
    
    # 這是一個簡化的 schema，適用於一般的新聞網站
    simple_news_schema = {
        "name": "General News Site",
        "baseSelector": "article, .article, .news-item, .post",
        "fields": [
            {"name": "title", "selector": "h1, h2, h3, .title, .headline", "type": "text"},
            {"name": "content", "selector": "p, .content, .article-body", "type": "text"},
            {"name": "date", "selector": ".date, .time, .published", "type": "text"},
            {"name": "author", "selector": ".author, .writer, .by", "type": "text"}
        ]
    }
    
    # 你可以替換成任何想要測試的新聞網站
    test_urls = [
        "https://news.ltn.com.tw/",  # 自由時報
        "https://www.chinatimes.com/",  # 中時新聞網
        "https://udn.com/news/index"  # 聯合新聞網
    ]
    
    print("建議測試的台灣新聞網站：")
    for i, url in enumerate(test_urls, 1):
        print(f"{i}. {url}")
    
    print("\n💡 使用建議：")
    print("1. 先用開發者工具檢查目標網站的HTML結構")
    print("2. 根據實際的CSS選擇器調整schema")
    print("3. 注意網站的反爬蟲機制，適當設置user_agent和延遲")
    print("4. 測試時建議先用小範圍的選擇器驗證")

def main():
    """主程式"""
    print("🚀 crawl4ai 完整教學案例")
    print("這個範例將教你如何使用不同的提取類型")
    
    # 執行教學案例
    asyncio.run(tutorial_extraction())
    
    # 顯示真實網站使用建議
    asyncio.run(real_website_example())

if __name__ == "__main__":
    main()