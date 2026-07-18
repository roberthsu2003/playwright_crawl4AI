"""
第十章：登入與 Cookie 處理 - 完整示範
展示 Playwright 的登入自動化、Cookie 管理和 Session 保存功能
"""

from playwright.sync_api import sync_playwright
import os
import json
from pathlib import Path


def get_html_path():
    """取得 HTML 檔案的絕對路徑"""
    current_dir = Path(__file__).parent
    html_path = current_dir / "login_demo.html"
    return f"file://{html_path.absolute()}"


def get_output_dir():
    """取得輸出目錄"""
    current_dir = Path(__file__).parent
    output_dir = current_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def demo_1_basic_login(page):
    """示範 1：基本登入流程"""
    print("\n" + "=" * 60)
    print("示範 1：基本登入流程")
    print("=" * 60)
    
    # 確保在登入頁面
    html_path = get_html_path()
    page.goto(html_path)
    page.wait_for_load_state("networkidle")
    
    # 檢查是否已登入，如果是則先登出
    if page.locator("#dashboard").is_visible():
        page.click("#logoutBtn")
        page.wait_for_timeout(500)
        print("✓ 已登出先前的登入狀態")
    
    # 填寫登入表單
    page.fill("#username", "admin")
    print("✓ 已填寫用戶名：admin")
    
    page.fill("#password", "password123")
    print("✓ 已填寫密碼：********")
    
    # 勾選「記住我」
    page.check("#rememberMe")
    print("✓ 已勾選「記住我」")
    
    # 點擊登入按鈕
    page.click(".login-btn")
    print("✓ 已點擊登入按鈕")
    
    # 等待登入完成
    page.wait_for_selector("#dashboard.show", timeout=5000)
    print("✓ 登入成功！")
    
    # 取得歡迎訊息
    welcome = page.locator("#welcomeUser").inner_text()
    print(f"✓ 歡迎訊息：{welcome}")


def demo_2_save_cookies(context, output_dir):
    """示範 2：儲存 Cookie"""
    print("\n" + "=" * 60)
    print("示範 2：儲存 Cookie")
    print("=" * 60)
    
    # 取得所有 Cookie
    cookies = context.cookies()
    
    print(f"✓ 取得 {len(cookies)} 個 Cookie：")
    for cookie in cookies:
        print(f"  - {cookie['name']}: {cookie['value'][:20]}...")
    
    # 儲存 Cookie 到 JSON 檔案
    cookies_file = output_dir / "cookies.json"
    with open(cookies_file, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Cookie 已儲存至：{cookies_file.name}")
    
    return cookies_file


def demo_3_load_cookies(browser, output_dir):
    """示範 3：載入 Cookie 重複登入"""
    print("\n" + "=" * 60)
    print("示範 3：載入已儲存的 Cookie")
    print("=" * 60)
    
    cookies_file = output_dir / "cookies.json"
    
    if not cookies_file.exists():
        print("❌ Cookie 檔案不存在，請先執行示範 1 和 2")
        return None
    
    # 載入 Cookie
    with open(cookies_file, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    
    print(f"✓ 從檔案載入 {len(cookies)} 個 Cookie")
    
    # 建立新的 context 並載入 Cookie
    context = browser.new_context()
    context.add_cookies(cookies)
    print("✓ Cookie 已載入到新的瀏覽器上下文")
    
    # 建立新頁面
    page = context.new_page()
    
    # 訪問頁面（應該會自動登入）
    html_path = get_html_path()
    page.goto(html_path)
    page.wait_for_load_state("networkidle")
    
    # 檢查是否自動登入
    if page.locator("#dashboard.show").is_visible():
        welcome = page.locator("#welcomeUser").inner_text()
        print(f"✓ 使用 Cookie 自動登入成功！歡迎：{welcome}")
    else:
        print("ℹ️  Cookie 可能已過期或無效")
    
    return context, page


def demo_4_save_storage_state(context, output_dir):
    """示範 4：儲存完整瀏覽器狀態"""
    print("\n" + "=" * 60)
    print("示範 4：儲存完整瀏覽器狀態（含 localStorage）")
    print("=" * 60)
    
    state_file = output_dir / "browser_state.json"
    
    # 儲存完整狀態（包含 Cookie 和 localStorage）
    context.storage_state(path=str(state_file))
    
    print(f"✓ 瀏覽器狀態已儲存至：{state_file.name}")
    
    # 顯示檔案大小
    file_size = state_file.stat().st_size
    print(f"✓ 檔案大小：{file_size} bytes")
    
    return state_file


def demo_5_login_flow_complete(browser, output_dir):
    """示範 5：完整登入流程（檢查狀態並登入）"""
    print("\n" + "=" * 60)
    print("示範 5：完整登入流程（含狀態檢查）")
    print("=" * 60)
    
    state_file = output_dir / "browser_state.json"
    
    # 嘗試使用已儲存的狀態
    if state_file.exists():
        print("✓ 找到已儲存的狀態檔案，嘗試重新使用...")
        try:
            context = browser.new_context(storage_state=str(state_file))
            page = context.new_page()
            
            html_path = get_html_path()
            page.goto(html_path)
            page.wait_for_load_state("networkidle")
            
            if page.locator("#dashboard.show").is_visible():
                print("✓ 使用已儲存的狀態成功登入！")
                return context, page
            else:
                print("ℹ️  狀態已過期，需要重新登入")
                context.close()
        except Exception as e:
            print(f"ℹ️  載入狀態失敗：{e}")
    
    # 需要重新登入
    print("\n開始新的登入流程...")
    context = browser.new_context()
    page = context.new_page()
    
    html_path = get_html_path()
    page.goto(html_path)
    page.wait_for_load_state("networkidle")
    
    # 執行登入
    page.fill("#username", "admin")
    page.fill("#password", "password123")
    page.check("#rememberMe")
    page.click(".login-btn")
    
    page.wait_for_selector("#dashboard.show", timeout=5000)
    print("✓ 登入成功")
    
    # 儲存狀態供下次使用
    context.storage_state(path=str(state_file))
    print(f"✓ 狀態已儲存")
    
    return context, page


def demo_6_scrape_member_data(page):
    """示範 6：登入後爬取會員資料"""
    print("\n" + "=" * 60)
    print("示範 6：登入後爬取會員資料")
    print("=" * 60)
    
    # 確保已登入
    if not page.locator("#dashboard.show").is_visible():
        print("❌ 尚未登入，無法爬取會員資料")
        return None
    
    # 爬取會員資料
    member_data = {
        "username": page.locator("#welcomeUser").inner_text(),
        "last_login": page.locator("#lastLogin").inner_text(),
        "points": page.locator("#pointsValue").inner_text(),
        "orders": page.locator("#ordersValue").inner_text(),
        "coupons": page.locator("#couponsValue").inner_text()
    }
    
    # 爬取最近活動
    activities = []
    activity_items = page.locator("#activityList li").all()
    for item in activity_items:
        activity = item.locator("span").first.inner_text()
        time = item.locator(".activity-time").inner_text()
        activities.append({"activity": activity, "time": time})
    
    member_data["activities"] = activities
    
    print("✓ 會員資料：")
    print(f"  用戶名：{member_data['username']}")
    print(f"  上次登入：{member_data['last_login']}")
    print(f"  積分：{member_data['points']}")
    print(f"  訂單數：{member_data['orders']}")
    print(f"  優惠券：{member_data['coupons']}")
    print(f"  最近活動：{len(activities)} 項")
    
    return member_data


def main():
    """主程式"""
    print("\n" + "🔐 " + "=" * 58)
    print("🔐  Playwright 登入與 Cookie 處理 - 完整示範")
    print("🔐 " + "=" * 58)
    
    output_dir = get_output_dir()
    print(f"\n📁 輸出目錄：{output_dir}")
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        
        context = browser.new_context()
        page = context.new_page()
        
        # 載入示範頁面
        html_path = get_html_path()
        print(f"\n📄 載入頁面：{html_path}")
        
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        print("✓ 頁面載入完成")
        
        try:
            # 執行示範
            demo_1_basic_login(page)
            page.wait_for_timeout(1000)
            
            demo_2_save_cookies(context, output_dir)
            page.wait_for_timeout(1000)
            
            demo_4_save_storage_state(context, output_dir)
            page.wait_for_timeout(1000)
            
            demo_6_scrape_member_data(page)
            page.wait_for_timeout(1000)
            
            # 關閉當前 context
            context.close()
            
            # 測試載入 Cookie
            print("\n" + "-" * 60)
            print("開啟新的瀏覽器視窗測試 Cookie 載入...")
            print("-" * 60)
            
            result = demo_3_load_cookies(browser, output_dir)
            if result:
                new_context, new_page = result
                page.wait_for_timeout(2000)
                new_context.close()
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        # 完成
        print("\n" + "=" * 60)
        print("✅ 所有示範完成！")
        print(f"📁 Cookie 和狀態檔案儲存於：{output_dir}")
        print("=" * 60)
        print("\n按 Enter 關閉瀏覽器...")
        input()
        
        browser.close()


if __name__ == "__main__":
    main()
