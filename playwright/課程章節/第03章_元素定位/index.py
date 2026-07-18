from playwright.sync_api import sync_playwright
import os

def element_location_demo():
    """
    元素定位示範程式
    展示四種不同的元素定位方法
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 取得當前檔案的絕對路徑
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(current_dir, "login_demo.html")
        
        # 開啟本地 HTML 檔案
        page.goto(f"file://{html_file}")
        print("✓ 已開啟登入頁面")
        
        # 方法1：使用 get_by_label() - 根據 label 文字定位
        print("\n使用 get_by_label() 定位輸入欄位...")
        page.get_by_label("用戶名").fill("admin")
        print("✓ 已填入用戶名：admin")
        
        page.get_by_label("密碼").fill("password")
        print("✓ 已填入密碼：password")
        
        # 方法2：使用 get_by_role() - 根據元素角色定位
        print("\n使用 get_by_role() 定位按鈕...")
        page.get_by_role("button", name="登入").click()
        print("✓ 已點擊登入按鈕")
        
        # 等待一下看到登入成功的訊息
        page.wait_for_timeout(3000)
        print("\n✓ 登入成功！")
        
        # === 以下是其他定位方法的示範（已註解） ===
        
        # 方法3：使用 CSS 選擇器
        # print("\n使用 CSS 選擇器定位...")
        # page.locator("#username").fill("admin")
        # page.locator("#password").fill("password")
        # page.locator("#login-button").click()
        
        # 方法4：使用 XPath
        # print("\n使用 XPath 定位...")
        # page.locator("xpath=//input[@id='username']").fill("admin")
        # page.locator("xpath=//input[@id='password']").fill("password")
        # page.locator("xpath=//button[text()='登入']").click()
        
        print("\n程式執行完成，3 秒後關閉瀏覽器...")
        page.wait_for_timeout(3000)
        
        browser.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Playwright 元素定位示範")
    print("=" * 60)
    element_location_demo()
    print("\n" + "=" * 60)
    print("示範完成！")
    print("=" * 60)
