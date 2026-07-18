"""
第十一章：反爬蟲對策 - 完整示範
展示 Playwright 的反爬蟲對策和隱藏自動化特徵的技巧
"""

from playwright.sync_api import sync_playwright
import os
import random
import time
from pathlib import Path


def get_html_path():
    """取得 HTML 檔案的絕對路徑"""
    current_dir = Path(__file__).parent
    html_path = current_dir / "anti_detection_demo.html"
    return f"file://{html_path.absolute()}"


def demo_1_basic_detection(page):
    """示範 1：基本檢測（未隱藏特徵）"""
    print("\n" + "=" * 60)
    print("示範 1：基本檢測（未隱藏特徵）")
    print("=" * 60)
    
    # 載入檢測頁面
    html_path = get_html_path()
    page.goto(html_path)
    page.wait_for_load_state("networkidle")
    
    # 等待自動檢測完成
    page.wait_for_timeout(1000)
    
    # 取得檢測分數
    score = page.locator("#scoreDisplay").inner_text()
    message = page.locator("#scoreMessage").inner_text()
    
    print(f"✓ 檢測分數：{score}")
    print(f"✓ 檢測結果：{message}")
    
    # 取得詳細結果
    results = page.locator(".detection-item").all()
    print("\n詳細檢測結果：")
    for result in results:
        name = result.locator("strong").inner_text()
        status = result.locator(".status-badge").inner_text()
        print(f"  - {name}: {status}")


def demo_2_simulate_human_behavior(page):
    """示範 2：模擬人類行為"""
    print("\n" + "=" * 60)
    print("示範 2：模擬人類行為")
    print("=" * 60)
    
    # 模擬隨機滑鼠移動
    print("\n模擬滑鼠移動...")
    tracker = page.locator("#mouseTracker")
    box = tracker.bounding_box()
    
    if box:
        for _ in range(5):
            x = box["x"] + random.randint(10, int(box["width"]) - 10)
            y = box["y"] + random.randint(10, int(box["height"]) - 10)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.1, 0.3))
    
    move_count = page.locator("#moveCount").inner_text()
    print(f"✓ 滑鼠移動次數：{move_count}")
    
    # 模擬隨機滾動
    print("\n模擬滾動...")
    for _ in range(3):
        scroll_amount = random.randint(100, 300)
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        time.sleep(random.uniform(0.3, 0.8))
    
    scroll_count = page.locator("#scrollCount").inner_text()
    print(f"✓ 滾動次數：{scroll_count}")
    
    # 模擬隨機點擊
    print("\n模擬點擊...")
    page.click("#simulateRequest")
    time.sleep(random.uniform(0.5, 1.0))
    page.click("#simulateRequest")
    time.sleep(random.uniform(0.3, 0.7))
    page.click("#simulateRequest")
    
    click_count = page.locator("#clickCount").inner_text()
    print(f"✓ 點擊次數：{click_count}")
    
    # 模擬按鍵
    print("\n模擬按鍵輸入...")
    page.keyboard.press("Tab")
    time.sleep(0.2)
    page.keyboard.press("Space")
    
    key_count = page.locator("#keyCount").inner_text()
    print(f"✓ 按鍵次數：{key_count}")


def demo_3_random_delay():
    """示範 3：隨機延遲策略"""
    print("\n" + "=" * 60)
    print("示範 3：隨機延遲策略")
    print("=" * 60)
    
    print("\n模擬多次請求的隨機延遲：")
    delays = []
    
    for i in range(5):
        # 使用不同的延遲策略
        if i == 0:
            delay = 0
        else:
            # 1-3 秒的隨機延遲
            delay = random.uniform(1, 3)
        
        delays.append(delay)
        print(f"  請求 {i+1}：等待 {delay:.2f} 秒")
        time.sleep(min(delay, 0.5))  # 實際示範時縮短等待
    
    avg_delay = sum(delays) / len(delays)
    print(f"\n✓ 平均延遲：{avg_delay:.2f} 秒")
    print("✓ 隨機延遲可以避免被識別為機器人")


def demo_4_stealth_browser():
    """示範 4：隱藏自動化特徵"""
    print("\n" + "=" * 60)
    print("示範 4：隱藏自動化特徵")
    print("=" * 60)
    
    with sync_playwright() as p:
        # 使用隱藏特徵的設定啟動瀏覽器
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--no-sandbox'
            ]
        )
        
        # 設定更真實的瀏覽器上下文
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='zh-TW',
            timezone_id='Asia/Taipei',
            geolocation={'longitude': 121.5654, 'latitude': 25.0330},
            permissions=['geolocation']
        )
        
        page = context.new_page()
        
        # 隱藏 WebDriver 特徵
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // 隱藏自動化相關的屬性
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // 模擬真實的語言設定
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-TW', 'zh', 'en-US', 'en']
            });
        """)
        
        print("✓ 已應用隱藏特徵設定：")
        print("  - 隱藏 WebDriver 屬性")
        print("  - 設定真實 User-Agent")
        print("  - 設定正常視窗大小")
        print("  - 設定語言和時區")
        
        # 載入檢測頁面
        html_path = get_html_path()
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        
        # 取得檢測分數
        score = page.locator("#scoreDisplay").inner_text()
        message = page.locator("#scoreMessage").inner_text()
        
        print(f"\n✓ 隱藏特徵後的檢測分數：{score}")
        print(f"✓ 檢測結果：{message}")
        
        page.wait_for_timeout(2000)
        
        context.close()
        browser.close()


def demo_5_user_agent_rotation():
    """示範 5：User-Agent 輪換"""
    print("\n" + "=" * 60)
    print("示範 5：User-Agent 輪換策略")
    print("=" * 60)
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    viewports = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1440, 'height': 900},
        {'width': 1536, 'height': 864},
        {'width': 1280, 'height': 720}
    ]
    
    print("可用的 User-Agent 列表：")
    for i, ua in enumerate(user_agents, 1):
        print(f"  {i}. {ua[:60]}...")
    
    print("\n可用的視窗大小：")
    for i, vp in enumerate(viewports, 1):
        print(f"  {i}. {vp['width']} x {vp['height']}")
    
    # 隨機選擇
    selected_ua = random.choice(user_agents)
    selected_vp = random.choice(viewports)
    
    print(f"\n✓ 隨機選擇的 User-Agent：{selected_ua[:60]}...")
    print(f"✓ 隨機選擇的視窗大小：{selected_vp['width']} x {selected_vp['height']}")


def main():
    """主程式"""
    print("\n" + "🛡️ " + "=" * 58)
    print("🛡️  Playwright 反爬蟲對策 - 完整示範")
    print("🛡️ " + "=" * 58)
    
    with sync_playwright() as p:
        # 啟動基本瀏覽器
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )
        
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # 執行示範
            demo_1_basic_detection(page)
            page.wait_for_timeout(1500)
            
            demo_2_simulate_human_behavior(page)
            page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        context.close()
        browser.close()
    
    # 獨立示範
    demo_3_random_delay()
    demo_5_user_agent_rotation()
    
    # 隱藏特徵示範
    print("\n" + "-" * 60)
    print("準備示範隱藏自動化特徵...")
    print("-" * 60)
    
    try:
        demo_4_stealth_browser()
    except Exception as e:
        print(f"\n❌ 發生錯誤：{e}")
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 所有示範完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
