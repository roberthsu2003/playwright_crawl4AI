"""
PTT 熱門文章爬蟲
適合 Python 初學者練習 Playwright
使用簡單的函式結構，不使用類別
"""

from playwright.sync_api import sync_playwright
import csv
from datetime import datetime
import os


def scrape_ptt_articles(board="Gossiping", max_articles=20, headless=False):
    """
    爬取 PTT 看板的文章列表

    參數說明:
        board (str): 看板名稱，例如 "Gossiping"、"Tech_Job"、"Beauty"
        max_articles (int): 要爬取的文章數量
        headless (bool): 是否使用無頭模式（False=顯示瀏覽器，True=背景執行）

    返回:
        list: 包含文章資料的列表，每個元素是一個字典
    """
    print(f"🚀 開始爬取 PTT {board} 看板...")
    print(f"📊 目標數量: {max_articles} 篇文章")

    # 用來儲存所有文章的列表
    articles_data = []

    with sync_playwright() as p:
        # 步驟 1: 啟動瀏覽器
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # 步驟 2: 前往看板頁面
        base_url = "https://www.ptt.cc"
        url = f"{base_url}/bbs/{board}/index.html"
        print(f"🌐 正在開啟: {url}")
        page.goto(url)

        # 步驟 3: 處理 18 歲確認頁面（某些看板需要）
        try:
            # 等待按鈕出現（最多等 3 秒）
            page.wait_for_selector("button.btn-big", timeout=3000)
            if page.locator("button:has-text('我同意')").is_visible():
                print("⚠️  偵測到年齡確認頁面，自動點擊「我同意」")
                page.click("button:has-text('我同意')")
                page.wait_for_load_state("networkidle")
        except:
            # 如果沒有出現確認頁面，就跳過
            pass

        # 步驟 4: 等待文章列表載入
        page.wait_for_selector("div.r-ent")
        print("✅ 頁面載入完成！")

        # 步驟 5: 開始擷取文章
        print("📝 開始擷取文章資料...")
        articles = page.locator("div.r-ent").all()

        count = 0
        for article in articles:
            # 如果已經抓到足夠數量，就停止
            if count >= max_articles:
                break

            try:
                # 5.1 擷取推文數
                push_elem = article.locator("div.nrec")
                push_count = push_elem.inner_text() if push_elem.is_visible() else "0"

                # 5.2 擷取標題（檢查文章是否存在）
                title_elem = article.locator("div.title a")
                if not title_elem.is_visible():
                    # 跳過已刪除的文章
                    continue
                title = title_elem.inner_text()

                # 5.3 擷取作者
                author = article.locator("div.author").inner_text()

                # 5.4 擷取日期
                date = article.locator("div.date").inner_text()

                # 5.5 將資料存成字典
                article_data = {
                    "推文數": push_count,
                    "標題": title,
                    "作者": author,
                    "日期": date,
                }

                # 5.6 加入到列表中
                articles_data.append(article_data)
                count += 1

                # 顯示進度
                print(f"  [{count}/{max_articles}] {push_count:>3} | {title[:40]}")

            except Exception as e:
                print(f"⚠️  擷取文章時發生錯誤: {e}")
                continue

        # 步驟 6: 關閉瀏覽器
        browser.close()

    print(f"✅ 成功爬取 {len(articles_data)} 篇文章！")
    return articles_data


def save_to_csv(articles_data, board="Gossiping", filename=None):
    """
    將文章資料儲存為 CSV 檔案

    參數說明:
        articles_data (list): 文章資料列表
        board (str): 看板名稱（用於產生檔名）
        filename (str): 指定檔案名稱（可選）

    返回:
        str: 儲存的檔案路徑
    """
    if not articles_data:
        print("❌ 沒有資料可以儲存")
        return None

    # 步驟 1: 建立 output 資料夾
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 建立輸出資料夾: {output_dir}")

    # 步驟 2: 產生檔案名稱（如果沒有指定）
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ptt_{board}_{timestamp}.csv"

    filepath = os.path.join(output_dir, filename)

    # 步驟 3: 寫入 CSV 檔案
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        # CSV 的欄位名稱
        fieldnames = ["推文數", "標題", "作者", "日期"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # 寫入標題列
        writer.writeheader()
        # 寫入所有資料
        writer.writerows(articles_data)

    print(f"💾 資料已儲存至: {filepath}")
    print(f"📊 共 {len(articles_data)} 筆資料")

    return filepath


def show_statistics(articles_data):
    """
    顯示文章的統計資訊

    參數說明:
        articles_data (list): 文章資料列表
    """
    if not articles_data:
        print("❌ 沒有資料可以分析")
        return

    print("\n" + "="*50)
    print("📊 統計資訊")
    print("="*50)
    print(f"總文章數: {len(articles_data)}")

    # 步驟 1: 統計推文數
    push_counts = []
    for article in articles_data:
        push_str = article["推文數"]
        # 將推文數轉換成數字
        if push_str.isdigit():
            push_counts.append(int(push_str))
        elif push_str == "爆":
            push_counts.append(100)  # 爆文設為 100

    # 步驟 2: 計算平均值和最大值
    if push_counts:
        average = sum(push_counts) / len(push_counts)
        maximum = max(push_counts)
        print(f"平均推文數: {average:.1f}")
        print(f"最高推文數: {maximum}")

    # 步驟 3: 找出最熱門的文章 TOP 3
    print("\n🔥 最熱門文章 TOP 3:")

    # 將文章按推文數排序（由高到低）
    sorted_articles = sorted(
        articles_data,
        key=lambda x: 100 if x["推文數"] == "爆" else (int(x["推文數"]) if x["推文數"].isdigit() else 0),
        reverse=True
    )

    # 顯示前 3 名
    for i, article in enumerate(sorted_articles[:3], 1):
        print(f"{i}. [{article['推文數']:>3}] {article['標題'][:50]}")

    print("="*50 + "\n")


def main():
    """
    主程式：執行完整的爬蟲流程
    """
    print("="*60)
    print(" "*15 + "PTT 熱門文章爬蟲")
    print("="*60 + "\n")

    # ========== 步驟 1: 設定爬蟲參數 ==========
    board_name = "Gossiping"  # 可以改成其他看板：Tech_Job, Soft_Job, Beauty 等
    article_count = 20        # 要爬取的文章數量
    show_browser = True       # True=顯示瀏覽器，False=背景執行

    # ========== 步驟 2: 開始爬取文章 ==========
    articles = scrape_ptt_articles(
        board=board_name,
        max_articles=article_count,
        headless=not show_browser  # headless=False 表示顯示瀏覽器
    )

    # ========== 步驟 3: 顯示統計資訊 ==========
    show_statistics(articles)

    # ========== 步驟 4: 儲存為 CSV 檔案 ==========
    save_to_csv(articles, board=board_name)

    print("\n✨ 程式執行完成！")
    print("💡 提示：可以用 Excel 或 Google Sheets 開啟 CSV 檔案查看資料\n")


# 當直接執行此程式時，會執行 main() 函式
if __name__ == "__main__":
    main()
