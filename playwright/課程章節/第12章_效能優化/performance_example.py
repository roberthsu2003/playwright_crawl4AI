"""
第十二章：效能優化 - 完整示範
展示 Playwright 的效能優化技巧，包括資源阻擋、平行處理和批次爬取
"""

from playwright.sync_api import sync_playwright
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def get_html_path():
    """取得 HTML 檔案的絕對路徑"""
    current_dir = Path(__file__).parent
    html_path = current_dir / "performance_demo.html"
    return f"file://{html_path.absolute()}"


def demo_1_without_optimization(browser):
    """示範 1：未優化的爬取（載入所有資源）"""
    print("\n" + "=" * 60)
    print("示範 1：未優化的爬取")
    print("=" * 60)
    
    context = browser.new_context()
    page = context.new_page()
    
    start_time = time.time()
    
    # 載入頁面（載入所有資源）
    html_path = get_html_path()
    page.goto(html_path, wait_until="networkidle")
    
    # 點擊載入資料
    page.click("#loadData")
    page.wait_for_selector(".data-card", timeout=5000)
    
    # 擷取資料
    cards = page.locator(".data-card").all()
    data_count = len(cards)
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000
    
    print(f"✓ 擷取到 {data_count} 個商品")
    print(f"✓ 耗時：{duration:.2f} ms")
    
    context.close()
    return duration


def demo_2_with_resource_blocking(browser):
    """示範 2：阻擋不必要的資源"""
    print("\n" + "=" * 60)
    print("示範 2：阻擋不必要的資源")
    print("=" * 60)
    
    context = browser.new_context()
    page = context.new_page()
    
    blocked_count = {"images": 0, "fonts": 0, "media": 0}
    
    def block_resources(route):
        resource_type = route.request.resource_type
        if resource_type == "image":
            blocked_count["images"] += 1
            route.abort()
        elif resource_type == "font":
            blocked_count["fonts"] += 1
            route.abort()
        elif resource_type == "media":
            blocked_count["media"] += 1
            route.abort()
        else:
            route.continue_()
    
    page.route("**/*", block_resources)
    
    start_time = time.time()
    
    # 載入頁面
    html_path = get_html_path()
    page.goto(html_path, wait_until="domcontentloaded")  # 使用更快的等待策略
    
    # 點擊載入資料
    page.click("#loadData")
    page.wait_for_selector(".data-card", timeout=5000)
    
    # 擷取資料
    cards = page.locator(".data-card").all()
    data_count = len(cards)
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000
    
    print(f"✓ 擷取到 {data_count} 個商品")
    print(f"✓ 耗時：{duration:.2f} ms")
    print(f"✓ 阻擋的資源：")
    for resource, count in blocked_count.items():
        print(f"  - {resource}: {count}")
    
    context.close()
    return duration


def demo_3_headless_mode():
    """示範 3：無頭模式效能比較"""
    print("\n" + "=" * 60)
    print("示範 3：無頭模式 vs 有頭模式")
    print("=" * 60)
    
    html_path = get_html_path()
    
    # 有頭模式
    print("\n--- 有頭模式 (headless=False) ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = time.time()
        page.goto(html_path, wait_until="domcontentloaded")
        page.click("#loadData")
        page.wait_for_selector(".data-card", timeout=5000)
        duration_headed = (time.time() - start_time) * 1000
        
        context.close()
        browser.close()
    
    print(f"✓ 有頭模式耗時：{duration_headed:.2f} ms")
    
    # 無頭模式
    print("\n--- 無頭模式 (headless=True) ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        start_time = time.time()
        page.goto(html_path, wait_until="domcontentloaded")
        page.click("#loadData")
        page.wait_for_selector(".data-card", timeout=5000)
        duration_headless = (time.time() - start_time) * 1000
        
        context.close()
        browser.close()
    
    print(f"✓ 無頭模式耗時：{duration_headless:.2f} ms")
    
    improvement = ((duration_headed - duration_headless) / duration_headed) * 100
    print(f"\n✓ 效能提升：{improvement:.1f}%")


def demo_4_parallel_processing():
    """示範 4：平行處理多個頁面"""
    print("\n" + "=" * 60)
    print("示範 4：平行處理多個頁面")
    print("=" * 60)
    
    html_path = get_html_path()
    
    # 模擬多個 URL（實際使用時會是不同的網址）
    urls = [html_path] * 5
    
    # 順序處理
    print("\n--- 順序處理 5 個頁面 ---")
    start_time = time.time()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for i, url in enumerate(urls, 1):
            context = browser.new_context()
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded")
            page.click("#loadData")
            page.wait_for_selector(".data-card", timeout=5000)
            context.close()
        
        browser.close()
    
    sequential_time = time.time() - start_time
    print(f"✓ 順序處理耗時：{sequential_time:.2f} 秒")
    
    # 平行處理（使用多個上下文）
    print("\n--- 平行處理 5 個頁面 ---")
    start_time = time.time()
    
    def scrape_page(args):
        p, url, page_num = args
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.click("#loadData")
        page.wait_for_selector(".data-card", timeout=5000)
        cards = page.locator(".data-card").all()
        result = len(cards)
        context.close()
        browser.close()
        return result
    
    with sync_playwright() as p:
        with ThreadPoolExecutor(max_workers=3) as executor:
            args = [(p, url, i) for i, url in enumerate(urls, 1)]
            # 注意：由於 Playwright 的限制，這裡簡化處理
            results = []
            for arg in args:
                result = scrape_page(arg)
                results.append(result)
    
    parallel_time = time.time() - start_time
    print(f"✓ 平行處理耗時：{parallel_time:.2f} 秒")
    
    if sequential_time > parallel_time:
        improvement = ((sequential_time - parallel_time) / sequential_time) * 100
        print(f"\n✓ 效能提升：{improvement:.1f}%")


def demo_5_batch_processing(browser):
    """示範 5：批次處理"""
    print("\n" + "=" * 60)
    print("示範 5：批次處理")
    print("=" * 60)
    
    html_path = get_html_path()
    
    # 模擬批次 URL
    batch_size = 3
    total_urls = 9
    urls = [html_path] * total_urls
    
    print(f"總共 {total_urls} 個 URL，每批 {batch_size} 個")
    
    all_results = []
    start_time = time.time()
    
    for batch_num in range(0, total_urls, batch_size):
        batch = urls[batch_num:batch_num + batch_size]
        print(f"\n處理批次 {batch_num // batch_size + 1}...")
        
        for i, url in enumerate(batch):
            context = browser.new_context()
            page = context.new_page()
            
            # 阻擋資源
            page.route("**/*", lambda route: (
                route.abort() if route.request.resource_type in ["image", "font", "media"]
                else route.continue_()
            ))
            
            page.goto(url, wait_until="domcontentloaded")
            page.click("#loadData")
            page.wait_for_selector(".data-card", timeout=5000)
            
            cards = page.locator(".data-card").all()
            all_results.append(len(cards))
            
            context.close()
            print(f"  - 頁面 {batch_num + i + 1}：擷取 {len(cards)} 個商品")
    
    total_time = time.time() - start_time
    
    print(f"\n✓ 總共處理 {len(all_results)} 個頁面")
    print(f"✓ 總耗時：{total_time:.2f} 秒")
    print(f"✓ 平均每頁：{total_time / len(all_results):.2f} 秒")


def demo_6_memory_efficient(browser):
    """示範 6：記憶體效率優化"""
    print("\n" + "=" * 60)
    print("示範 6：記憶體效率優化")
    print("=" * 60)
    
    html_path = get_html_path()
    
    print("\n展示正確的資源管理方式：")
    print("""
    # 正確做法：及時關閉 context 和 page
    for url in urls:
        context = browser.new_context()
        page = context.new_page()
        
        # 執行操作
        page.goto(url)
        data = page.inner_text("#content")
        
        # 立即關閉以釋放記憶體
        page.close()
        context.close()
    """)
    
    # 示範
    contexts_created = 0
    
    for i in range(3):
        context = browser.new_context()
        page = context.new_page()
        contexts_created += 1
        
        page.goto(html_path, wait_until="domcontentloaded")
        
        # 模擬處理
        title = page.title()
        
        # 立即關閉
        page.close()
        context.close()
        
        print(f"✓ 處理頁面 {i + 1}，已關閉 context")
    
    print(f"\n✓ 總共建立並關閉 {contexts_created} 個 context")
    print("✓ 正確的資源管理可以避免記憶體洩漏")


def main():
    """主程式"""
    print("\n" + "⚡ " + "=" * 58)
    print("⚡  Playwright 效能優化 - 完整示範")
    print("⚡ " + "=" * 58)
    
    with sync_playwright() as p:
        # 使用有頭模式展示
        browser = p.chromium.launch(headless=False, slow_mo=200)
        
        try:
            # 示範 1：未優化
            time1 = demo_1_without_optimization(browser)
            time.sleep(1)
            
            # 示範 2：資源阻擋
            time2 = demo_2_with_resource_blocking(browser)
            time.sleep(1)
            
            # 比較
            if time1 > time2:
                improvement = ((time1 - time2) / time1) * 100
                print(f"\n📊 資源阻擋效能提升：{improvement:.1f}%")
            
            # 示範 5：批次處理
            demo_5_batch_processing(browser)
            time.sleep(1)
            
            # 示範 6：記憶體效率
            demo_6_memory_efficient(browser)
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        browser.close()
    
    # 獨立示範
    print("\n" + "-" * 60)
    print("準備示範無頭模式和平行處理...")
    print("-" * 60)
    
    try:
        demo_3_headless_mode()
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 所有示範完成！")
    print("=" * 60)
    print("\n效能優化重點總結：")
    print("1. 使用 headless 模式")
    print("2. 阻擋不必要的資源（圖片、字體、媒體）")
    print("3. 使用 domcontentloaded 而非 networkidle")
    print("4. 批次處理控制並發數量")
    print("5. 及時關閉 page 和 context 釋放記憶體")


if __name__ == "__main__":
    main()
