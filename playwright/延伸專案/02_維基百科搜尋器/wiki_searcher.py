"""
維基百科關鍵字搜尋器
適合 Python 初學者練習 Playwright 進階功能
使用簡單的函式結構，不使用類別
"""

from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime


def search_wiki_keyword(keyword, language="zh", headless=False):
    """
    在維基百科搜尋單一關鍵字

    參數說明:
        keyword (str): 要搜尋的關鍵字
        language (str): 語言代碼，'zh'=中文，'en'=英文
        headless (bool): 是否使用無頭模式（False=顯示瀏覽器）

    返回:
        dict: 包含條目資訊的字典，如果找不到則返回 None
    """
    print(f"\n🔍 正在搜尋: {keyword}")

    # 維基百科的網址
    base_url = f"https://{language}.wikipedia.org"

    with sync_playwright() as p:
        # 步驟 1: 啟動瀏覽器
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # 步驟 2: 前往維基百科首頁
        page.goto(base_url)
        print(f"  ✅ 已開啟 {base_url}")

        # 步驟 3: 找到搜尋框並輸入關鍵字
        search_box = page.locator("input[name='search']")
        search_box.fill(keyword)
        print(f"  ⌨️  輸入關鍵字: {keyword}")

        # 步驟 4: 按下 Enter 搜尋
        search_box.press("Enter")

        # 等待頁面載入完成
        page.wait_for_load_state("networkidle")

        # 步驟 5: 檢查是否找到條目
        try:
            title = page.locator("h1.firstHeading").inner_text()

            # 檢查是否為「查無此頁」
            if "不存在" in title or "does not exist" in title.lower():
                print(f"  ❌ 找不到條目: {keyword}")
                browser.close()
                return None

            print(f"  📄 找到條目: {title}")

        except:
            print(f"  ❌ 頁面載入失敗")
            browser.close()
            return None

        # 步驟 6: 建立基本資料結構
        result = {
            "keyword": keyword,
            "title": title,
            "url": page.url,
            "scraped_at": datetime.now().isoformat()
        }

        # 步驟 7: 擷取摘要
        print("  📝 擷取摘要...")
        result["summary"] = extract_summary(page)

        # 步驟 8: 擷取分類
        print("  🏷️  擷取分類...")
        result["categories"] = extract_categories(page)

        # 步驟 9: 擷取資訊框
        print("  📊 擷取資訊框...")
        result["infobox"] = extract_infobox(page)

        # 步驟 10: 擷取統計資訊
        print("  📈 擷取統計...")
        result["stats"] = extract_statistics(page)

        # 步驟 11: 關閉瀏覽器
        browser.close()
        print(f"  ✅ 完成！")

        return result


def extract_summary(page):
    """
    擷取維基百科條目的摘要段落

    參數說明:
        page: Playwright 的 page 物件

    返回:
        str: 摘要文字
    """
    try:
        # 找到內容區的所有段落
        paragraphs = page.locator("div.mw-parser-output > p").all()
        summary_parts = []

        # 取前兩個有實質內容的段落
        for p in paragraphs[:5]:  # 最多檢查前 5 個
            text = p.inner_text().strip()
            # 過濾太短的段落和座標提示
            if text and len(text) > 30 and "座標" not in text:
                summary_parts.append(text)
                # 如果已經有 2 段，就停止
                if len(summary_parts) >= 2:
                    break

        # 用兩個換行符號連接段落
        if summary_parts:
            return "\n\n".join(summary_parts)
        else:
            return "無摘要"

    except:
        return "擷取失敗"


def extract_categories(page):
    """
    擷取維基百科條目的分類標籤

    參數說明:
        page: Playwright 的 page 物件

    返回:
        list: 分類標籤列表
    """
    try:
        categories = []
        # 維基百科的分類通常在頁面底部
        cat_links = page.locator("#mw-normal-catlinks ul li a").all()

        # 最多取 10 個分類
        for link in cat_links[:10]:
            categories.append(link.inner_text())

        return categories

    except:
        return []


def extract_infobox(page):
    """
    擷取維基百科條目的資訊框資料

    參數說明:
        page: Playwright 的 page 物件

    返回:
        dict: 資訊框資料字典
    """
    try:
        infobox = {}

        # 檢查是否有資訊框
        if not page.locator("table.infobox").is_visible():
            return infobox

        # 擷取資訊框的每一行
        rows = page.locator("table.infobox tr").all()

        for row in rows:
            try:
                # 找標題（th）和內容（td）
                header = row.locator("th")
                data = row.locator("td")

                # 如果這一行有標題和內容
                if header.count() > 0 and data.count() > 0:
                    key = header.inner_text().strip()
                    value = data.inner_text().strip()

                    # 過濾空值和太長的內容
                    if key and value and len(value) < 200:
                        infobox[key] = value

            except:
                continue

        return infobox

    except:
        return {}


def extract_statistics(page):
    """
    擷取維基百科條目的統計資訊

    參數說明:
        page: Playwright 的 page 物件

    返回:
        dict: 統計資料字典
    """
    stats = {}

    try:
        # 計算外部連結數量
        external_links = page.locator("#外部連結 ~ ul a, #外部链接 ~ ul a").count()
        stats["external_links"] = external_links

        # 計算參考資料數量
        references = page.locator("ol.references li").count()
        stats["references"] = references

        # 計算章節數量
        headings = page.locator("h2").count()
        stats["sections"] = headings

    except:
        pass

    return stats


def search_multiple_keywords(keywords, language="zh", headless=False):
    """
    批次搜尋多個關鍵字

    參數說明:
        keywords (list): 關鍵字列表
        language (str): 語言代碼
        headless (bool): 是否使用無頭模式

    返回:
        list: 所有搜尋結果的列表
    """
    print("="*60)
    print(" "*15 + f"批次搜尋 {len(keywords)} 個關鍵字")
    print("="*60)

    results = []

    # 迴圈搜尋每個關鍵字
    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] ", end="")
        result = search_wiki_keyword(keyword, language=language, headless=headless)

        # 如果成功找到，加入結果列表
        if result:
            results.append(result)

    print("\n" + "="*60)
    print(f"✅ 搜尋完成！成功 {len(results)}/{len(keywords)} 個")
    print("="*60)

    return results


def save_to_json(results, language="zh", filename=None):
    """
    將搜尋結果儲存為 JSON 檔案

    參數說明:
        results (list): 搜尋結果列表
        language (str): 語言代碼（用於檔名）
        filename (str): 指定檔案名稱（可選）

    返回:
        str: 儲存的檔案路徑
    """
    if not results:
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
        filename = f"wiki_results_{timestamp}.json"

    filepath = os.path.join(output_dir, filename)

    # 步驟 3: 組織資料結構
    output_data = {
        "metadata": {
            "language": language,
            "total_results": len(results),
            "scraped_at": datetime.now().isoformat()
        },
        "results": results
    }

    # 步驟 4: 寫入 JSON 檔案
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"💾 資料已儲存至: {filepath}")
    print(f"📊 共 {len(results)} 筆資料")

    return filepath


def save_summary_report(results, filename=None):
    """
    產生並儲存文字摘要報告

    參數說明:
        results (list): 搜尋結果列表
        filename (str): 指定檔案名稱（可選）

    返回:
        str: 儲存的檔案路徑
    """
    if not results:
        print("❌ 沒有資料可以產生報告")
        return None

    # 步驟 1: 建立 output 資料夾
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 步驟 2: 產生檔案名稱（如果沒有指定）
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wiki_summary_{timestamp}.txt"

    filepath = os.path.join(output_dir, filename)

    # 步驟 3: 撰寫報告
    with open(filepath, "w", encoding="utf-8") as f:
        # 標題
        f.write("="*70 + "\n")
        f.write("維基百科搜尋摘要報告\n")
        f.write("="*70 + "\n\n")
        f.write(f"搜尋時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"總筆數: {len(results)}\n\n")

        # 每個搜尋結果的詳細資訊
        for i, result in enumerate(results, 1):
            f.write("-"*70 + "\n")
            f.write(f"[{i}] {result['title']}\n")
            f.write("-"*70 + "\n")
            f.write(f"關鍵字: {result['keyword']}\n")
            f.write(f"網址: {result['url']}\n\n")

            # 摘要
            f.write("📝 摘要:\n")
            f.write(result['summary'][:300] + "...\n\n")

            # 分類
            if result['categories']:
                f.write(f"🏷️  分類: {', '.join(result['categories'][:5])}\n\n")

            # 資訊框重點
            if result['infobox']:
                f.write("📊 資訊框重點:\n")
                for key, value in list(result['infobox'].items())[:5]:
                    f.write(f"  • {key}: {value}\n")
                f.write("\n")

            # 統計
            if result['stats']:
                f.write("📈 統計:\n")
                stats = result['stats']
                if 'references' in stats:
                    f.write(f"  • 參考資料: {stats['references']} 條\n")
                if 'sections' in stats:
                    f.write(f"  • 章節數: {stats['sections']} 個\n")
                if 'external_links' in stats:
                    f.write(f"  • 外部連結: {stats['external_links']} 個\n")
                f.write("\n")

    print(f"📄 摘要報告已儲存至: {filepath}")
    return filepath


def print_summary(results):
    """
    在終端機顯示搜尋結果摘要

    參數說明:
        results (list): 搜尋結果列表
    """
    if not results:
        print("❌ 沒有資料")
        return

    print("\n" + "="*60)
    print("📊 搜尋結果摘要")
    print("="*60)

    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result['title']}")
        print(f"    🔗 {result['url']}")
        print(f"    📝 {result['summary'][:100]}...")

        if result['stats']:
            stats = result['stats']
            print(f"    📈 參考: {stats.get('references', 0)} | "
                  f"章節: {stats.get('sections', 0)} | "
                  f"外部連結: {stats.get('external_links', 0)}")


def main():
    """
    主程式：執行完整的搜尋流程
    """
    print("="*70)
    print(" "*20 + "維基百科關鍵字搜尋器")
    print("="*70 + "\n")

    # ========== 步驟 1: 設定搜尋參數 ==========
    keywords = [
        "Python",
        "Playwright",
        "網頁爬蟲"
    ]
    wiki_language = "zh"      # 可改為 'en' 搜尋英文維基
    show_browser = True       # True=顯示瀏覽器，False=背景執行

    print(f"📋 搜尋清單: {', '.join(keywords)}")

    # ========== 步驟 2: 批次搜尋 ==========
    results = search_multiple_keywords(
        keywords,
        language=wiki_language,
        headless=not show_browser
    )

    # ========== 步驟 3: 顯示摘要 ==========
    print_summary(results)

    # ========== 步驟 4: 儲存結果 ==========
    save_to_json(results, language=wiki_language)
    save_summary_report(results)

    print("\n✨ 程式執行完成！")
    print("💡 提示：可以用文字編輯器開啟 output/ 資料夾中的檔案查看結果\n")


# 當直接執行此程式時，會執行 main() 函式
if __name__ == "__main__":
    main()
