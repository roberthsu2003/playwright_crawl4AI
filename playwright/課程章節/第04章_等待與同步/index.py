"""
第04章：等待與同步 - 完整示範
展示 Playwright 中各種等待策略的實際應用
"""

from playwright.sync_api import sync_playwright
import time
import os

def get_html_path():
    """取得 HTML 檔案的絕對路徑"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'waiting_demo.html')
    return f"file://{html_path}"

def demo_1_delayed_element(page):
    """示範 1：等待延遲載入的元素"""
    print("\n" + "="*60)
    print("示範 1：等待延遲載入的元素")
    print("="*60)
    
    # 點擊觸發按鈕
    page.click("#trigger-delayed")
    print("✓ 已點擊觸發按鈕")
    
    # 等待載入指示器出現
    page.wait_for_selector("#loading-1", state="visible")
    print("✓ 載入指示器已出現")
    
    # 等待載入指示器消失
    page.wait_for_selector("#loading-1", state="hidden")
    print("✓ 載入指示器已消失")
    
    # 等待結果元素出現
    page.wait_for_selector("#delayed-result.show", state="visible")
    print("✓ 延遲元素已成功載入")
    
    # 取得內容
    content = page.locator("#delayed-content").text_content()
    print(f"✓ 內容：{content}")

def demo_2_dynamic_content(page):
    """示範 2：等待動態內容載入（模擬 AJAX）"""
    print("\n" + "="*60)
    print("示範 2：等待動態內容載入")
    print("="*60)
    
    # 點擊載入資料按鈕
    page.click("#load-data")
    print("✓ 已點擊載入資料按鈕")
    
    # 等待載入指示器
    page.wait_for_selector("#loading-2", state="visible")
    print("✓ 正在載入資料...")
    
    # 等待資料載入完成
    page.wait_for_selector("#loading-2", state="hidden")
    print("✓ 資料載入完成")
    
    # 等待至少有 3 個項目出現
    page.wait_for_function(
        "document.querySelectorAll('#dynamic-content .item').length >= 3"
    )
    print("✓ 所有資料項目已載入")
    
    # 取得所有項目
    items = page.locator("#dynamic-content .item").all()
    print(f"✓ 共載入 {len(items)} 個項目：")
    for i, item in enumerate(items, 1):
        print(f"  {i}. {item.text_content()}")

def demo_3_visibility_toggle(page):
    """示範 3：等待元素狀態變化"""
    print("\n" + "="*60)
    print("示範 3：等待元素狀態變化")
    print("="*60)
    
    # 檢查初始狀態（隱藏）
    is_hidden = page.locator("#toggle-element").is_hidden()
    print(f"✓ 初始狀態：{'隱藏' if is_hidden else '可見'}")
    
    # 點擊切換按鈕
    page.click("#toggle-visibility")
    print("✓ 已點擊切換按鈕")
    
    # 等待元素變為可見
    page.wait_for_selector("#toggle-element", state="visible")
    print("✓ 元素現在可見")
    
    # 取得內容
    content = page.locator("#toggle-element").text_content()
    print(f"✓ 內容：{content}")
    
    # 再次切換回隱藏
    page.click("#toggle-visibility")
    page.wait_for_selector("#toggle-element", state="hidden")
    print("✓ 元素已隱藏")

def demo_4_form_submission(page):
    """示範 4：表單提交與等待"""
    print("\n" + "="*60)
    print("示範 4：表單提交與等待")
    print("="*60)
    
    # 填寫表單
    username = "Playwright 測試用戶"
    page.fill("#username", username)
    print(f"✓ 已填寫使用者名稱：{username}")
    
    # 提交表單
    page.click("#submit-form")
    print("✓ 已提交表單")
    
    # 等待處理中指示器
    page.wait_for_selector("#loading-3", state="visible")
    print("✓ 正在處理...")
    
    # 等待處理完成
    page.wait_for_selector("#loading-3", state="hidden")
    page.wait_for_selector("#form-result.show", state="visible")
    print("✓ 處理完成")
    
    # 取得提交訊息
    message = page.locator("#submit-message").text_content()
    print(f"✓ 回應訊息：{message}")

def demo_5_batch_loading(page):
    """示範 5：批次載入元素"""
    print("\n" + "="*60)
    print("示範 5：批次載入元素")
    print("="*60)
    
    # 點擊載入項目按鈕
    page.click("#load-items")
    print("✓ 開始載入項目...")
    
    # 等待第一個項目出現
    page.wait_for_selector("#items-container .item", state="visible")
    print("✓ 第一個項目已出現")
    
    # 等待所有 5 個項目載入完成
    page.wait_for_function(
        "document.querySelectorAll('#items-container .item').length >= 5"
    )
    print("✓ 所有項目載入完成")
    
    # 等待載入指示器消失
    page.wait_for_selector("#loading-4", state="hidden")
    
    # 取得所有項目
    items = page.locator("#items-container .item").all()
    print(f"✓ 共載入 {len(items)} 個項目")

def demo_6_api_request(page):
    """示範 6：等待 API 請求與回應"""
    print("\n" + "="*60)
    print("示範 6：等待 API 請求與回應")
    print("="*60)
    
    # 點擊 API 請求按鈕
    page.click("#api-request")
    print("✓ 已發送 API 請求")
    
    # 等待載入指示器
    page.wait_for_selector("#loading-5", state="visible")
    print("✓ 等待 API 回應...")
    
    # 等待回應完成
    page.wait_for_selector("#loading-5", state="hidden")
    page.wait_for_selector("#api-result.show", state="visible")
    print("✓ API 回應已接收")
    
    # 取得 API 回應內容
    response_text = page.locator("#api-response").text_content()
    print("✓ API 回應內容：")
    print(response_text)

def demo_7_load_states(page):
    """示範 7：不同的頁面載入狀態"""
    print("\n" + "="*60)
    print("示範 7：頁面載入狀態")
    print("="*60)
    
    html_path = get_html_path()
    
    # 重新載入頁面並觀察不同狀態
    print("✓ 重新載入頁面...")
    page.goto(html_path)
    
    # 等待 DOM 內容載入
    page.wait_for_load_state("domcontentloaded")
    print("✓ DOM 內容已載入")
    
    # 等待頁面完全載入
    page.wait_for_load_state("load")
    print("✓ 頁面完全載入")
    
    # 等待網路閒置
    page.wait_for_load_state("networkidle")
    print("✓ 網路已閒置")
    
    # 使用自訂函數等待
    page.wait_for_function("document.body.getAttribute('data-loaded') === 'true'")
    print("✓ 頁面載入完成標記已設定")

def demo_8_timeout_settings(page):
    """示範 8：超時時間設定"""
    print("\n" + "="*60)
    print("示範 8：超時時間設定")
    print("="*60)
    
    # 設定全域超時時間
    page.set_default_timeout(30000)  # 30 秒
    print("✓ 已設定全域超時時間：30 秒")
    
    # 使用自訂超時時間等待元素
    try:
        page.click("#trigger-delayed")
        page.wait_for_selector("#delayed-result.show", timeout=5000)
        print("✓ 在 5 秒內成功等待到元素")
    except Exception as e:
        print(f"✗ 等待超時：{e}")

def main():
    """主程式"""
    print("\n" + "🎯 " + "="*58)
    print("🎯  Playwright 等待與同步 - 完整示範")
    print("🎯 " + "="*58)
    
    with sync_playwright() as p:
        # 啟動瀏覽器（顯示模式）
        browser = p.chromium.launch(
            headless=False,
            slow_mo=500  # 放慢操作速度以便觀察
        )
        
        # 建立新頁面
        page = browser.new_page()
        
        # 設定預設超時時間
        page.set_default_timeout(30000)
        
        # 取得 HTML 檔案路徑
        html_path = get_html_path()
        print(f"\n📄 載入頁面：{html_path}")
        
        # 載入頁面
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        print("✓ 頁面載入完成\n")
        
        # 執行各個示範
        try:
            demo_1_delayed_element(page)
            time.sleep(1)
            
            demo_2_dynamic_content(page)
            time.sleep(1)
            
            demo_3_visibility_toggle(page)
            time.sleep(1)
            
            demo_4_form_submission(page)
            time.sleep(1)
            
            demo_5_batch_loading(page)
            time.sleep(1)
            
            demo_6_api_request(page)
            time.sleep(1)
            
            demo_7_load_states(page)
            time.sleep(1)
            
            demo_8_timeout_settings(page)
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        # 完成
        print("\n" + "="*60)
        print("✅ 所有示範完成！")
        print("="*60)
        print("\n按 Enter 關閉瀏覽器...")
        input()
        
        # 關閉瀏覽器
        browser.close()

if __name__ == "__main__":
    main()
