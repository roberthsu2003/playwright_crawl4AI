"""
第七章：多頁面與框架處理 - 完整示範
展示 Playwright 處理多頁面、彈出視窗、對話框和 iframe 的功能
"""

from playwright.sync_api import sync_playwright
import os


def get_html_path(filename):
    """取得 HTML 檔案的絕對路徑"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, filename)
    return f"file://{html_path}"


def demo_1_popup_window(context, main_page):
    """示範 1：處理彈出視窗"""
    print("\n" + "=" * 60)
    print("示範 1：處理彈出視窗 (Popup)")
    print("=" * 60)
    
    # 監聽新頁面（彈出視窗）
    with main_page.expect_popup() as popup_info:
        main_page.click("#openPopup")
    
    popup = popup_info.value
    popup.wait_for_load_state()
    
    print(f"✓ 彈出視窗標題：{popup.title()}")
    print(f"✓ 彈出視窗內容：{popup.locator('h2').inner_text()}")
    
    # 關閉彈出視窗
    popup.close()
    print("✓ 彈出視窗已關閉")
    
    # 檢查結果
    result = main_page.locator("#popupResult").inner_text()
    print(f"✓ 主頁面結果：{result}")


def demo_2_dialogs(page):
    """示範 2：處理對話框 (alert, confirm, prompt)"""
    print("\n" + "=" * 60)
    print("示範 2：處理對話框")
    print("=" * 60)
    
    # 2.1 處理 Alert
    print("\n--- 處理 Alert ---")
    
    def handle_alert(dialog):
        print(f"  對話框類型：{dialog.type}")
        print(f"  對話框訊息：{dialog.message}")
        dialog.accept()
    
    page.on("dialog", handle_alert)
    page.click("#showAlert")
    page.wait_for_timeout(500)
    
    result = page.locator("#dialogResult").inner_text()
    print(f"✓ 結果：{result}")
    
    # 移除監聽器
    page.remove_listener("dialog", handle_alert)
    
    # 2.2 處理 Confirm（點擊確認）
    print("\n--- 處理 Confirm（確認）---")
    
    def handle_confirm_accept(dialog):
        print(f"  對話框類型：{dialog.type}")
        print(f"  對話框訊息：{dialog.message}")
        dialog.accept()
    
    page.on("dialog", handle_confirm_accept)
    page.click("#showConfirm")
    page.wait_for_timeout(500)
    
    result = page.locator("#dialogResult").inner_text()
    print(f"✓ 結果：{result}")
    
    page.remove_listener("dialog", handle_confirm_accept)
    
    # 2.3 處理 Confirm（點擊取消）
    print("\n--- 處理 Confirm（取消）---")
    
    def handle_confirm_dismiss(dialog):
        dialog.dismiss()
    
    page.on("dialog", handle_confirm_dismiss)
    page.click("#showConfirm")
    page.wait_for_timeout(500)
    
    result = page.locator("#dialogResult").inner_text()
    print(f"✓ 結果：{result}")
    
    page.remove_listener("dialog", handle_confirm_dismiss)
    
    # 2.4 處理 Prompt
    print("\n--- 處理 Prompt ---")
    
    def handle_prompt(dialog):
        print(f"  對話框類型：{dialog.type}")
        print(f"  對話框訊息：{dialog.message}")
        dialog.accept("Playwright 使用者")
    
    page.on("dialog", handle_prompt)
    page.click("#showPrompt")
    page.wait_for_timeout(500)
    
    result = page.locator("#dialogResult").inner_text()
    print(f"✓ 結果：{result}")
    
    page.remove_listener("dialog", handle_prompt)


def demo_3_iframe(page):
    """示範 3：處理 iframe"""
    print("\n" + "=" * 60)
    print("示範 3：處理 iframe")
    print("=" * 60)
    
    # 使用 frame_locator 定位 iframe
    iframe = page.frame_locator("#myFrame")
    
    # 在 iframe 中填寫表單
    iframe.locator("#iframeName").fill("張三")
    print("✓ 已在 iframe 中填寫姓名：張三")
    
    iframe.locator("#iframeEmail").fill("zhang@example.com")
    print("✓ 已在 iframe 中填寫 Email：zhang@example.com")
    
    # 提交表單
    iframe.locator("#iframeSubmit").click()
    print("✓ 已在 iframe 中提交表單")
    
    # 等待父頁面收到訊息
    page.wait_for_timeout(1000)
    
    # 檢查父頁面的結果
    result = page.locator("#iframeResult").inner_text()
    print(f"✓ 父頁面收到的訊息：{result}")
    
    # 檢查 iframe 內的成功訊息
    success_visible = iframe.locator("#iframeSuccess").is_visible()
    print(f"✓ iframe 內顯示成功訊息：{success_visible}")


def demo_4_multiple_tabs(page):
    """示範 4：多分頁切換"""
    print("\n" + "=" * 60)
    print("示範 4：多分頁切換")
    print("=" * 60)
    
    # 點擊不同的分頁
    tabs = ["tab1", "tab2", "tab3"]
    
    for tab in tabs:
        page.click(f".tab-item[data-tab='{tab}']")
        page.wait_for_timeout(500)
        
        content = page.locator("#tabContent").inner_text()
        print(f"✓ {tab} 內容：{content}")


def demo_5_multiple_pages(context):
    """示範 5：在多個分頁之間操作"""
    print("\n" + "=" * 60)
    print("示範 5：在多個分頁之間操作")
    print("=" * 60)
    
    # 取得所有現有頁面
    print(f"✓ 目前有 {len(context.pages)} 個頁面")
    
    # 建立新頁面
    page2 = context.new_page()
    page2.goto("https://example.com")
    page2.wait_for_load_state("networkidle")
    print(f"✓ 開啟新頁面：{page2.title()}")
    
    page3 = context.new_page()
    page3.goto("https://example.org")
    page3.wait_for_load_state("networkidle")
    print(f"✓ 開啟新頁面：{page3.title()}")
    
    # 列出所有頁面
    print(f"\n目前共有 {len(context.pages)} 個頁面：")
    for i, p in enumerate(context.pages):
        print(f"  {i + 1}. {p.title()}")
    
    # 切換到第一個頁面
    context.pages[0].bring_to_front()
    print("\n✓ 已切換回第一個頁面")
    
    # 關閉額外的頁面
    page2.close()
    page3.close()
    print("✓ 已關閉額外的頁面")
    print(f"✓ 目前剩餘 {len(context.pages)} 個頁面")


def main():
    """主程式"""
    print("\n" + "🪟 " + "=" * 58)
    print("🪟  Playwright 多頁面與框架處理 - 完整示範")
    print("🪟 " + "=" * 58)
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )
        
        # 建立瀏覽器上下文
        context = browser.new_context()
        
        # 建立主頁面
        page = context.new_page()
        
        # 載入示範頁面
        html_path = get_html_path("multipage_demo.html")
        print(f"\n📄 載入頁面：{html_path}")
        
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        print("✓ 頁面載入完成\n")
        
        try:
            # 執行示範
            demo_1_popup_window(context, page)
            page.wait_for_timeout(1000)
            
            demo_2_dialogs(page)
            page.wait_for_timeout(1000)
            
            demo_3_iframe(page)
            page.wait_for_timeout(1000)
            
            demo_4_multiple_tabs(page)
            page.wait_for_timeout(1000)
            
            demo_5_multiple_pages(context)
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        # 完成
        print("\n" + "=" * 60)
        print("✅ 所有示範完成！")
        print("=" * 60)
        print("\n按 Enter 關閉瀏覽器...")
        input()
        
        # 關閉瀏覽器
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
