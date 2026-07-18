"""
第六章：進階互動範例
展示 Playwright 的進階互動功能，包括：
- 滑鼠懸停與下拉選單
- 各種點擊操作（單擊、雙擊、右鍵）
- 拖曳操作
- 鍵盤輸入
- 滾動操作
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time


def interactive_example():
    """執行進階互動範例"""
    with sync_playwright() as p:
        # 啟動瀏覽器（有頭模式，方便觀察）
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # 取得當前檔案的絕對路徑
        current_dir = Path(__file__).parent
        html_file = current_dir / "interactive_demo.html"
        
        # 訪問本地 HTML 檔案
        page.goto(f"file://{html_file.absolute()}")
        print("✅ 已開啟互動範例頁面\n")
        
        # ===== 1. 滑鼠懸停 - 下拉選單 =====
        print("=" * 50)
        print("1. 滑鼠懸停 - 下拉選單操作")
        print("=" * 50)
        
        # 懸停到下拉選單觸發按鈕
        page.hover("#menuTrigger")
        print("   - 已懸停到「選擇功能」按鈕")
        page.wait_for_timeout(1000)
        
        # 點擊下拉選單項目
        page.click("#dropdownMenu a[data-action='編輯']")
        print("   - 已點擊「編輯項目」選項")
        page.wait_for_timeout(1000)
        
        # ===== 2. 滑鼠點擊操作 =====
        print("\n" + "=" * 50)
        print("2. 滑鼠點擊操作")
        print("=" * 50)
        
        # 單擊
        page.click("#singleClick")
        print("   - 已執行單擊操作")
        page.wait_for_timeout(500)
        
        page.click("#singleClick")
        print("   - 再次單擊")
        page.wait_for_timeout(500)
        
        # 雙擊
        page.dblclick("#doubleClick")
        print("   - 已執行雙擊操作")
        page.wait_for_timeout(500)
        
        # 右鍵點擊
        page.click("#rightClick", button="right")
        print("   - 已執行右鍵點擊操作")
        page.wait_for_timeout(1000)
        
        # 點擊右鍵選單項目
        page.click(".context-menu-item[data-action='複製']")
        print("   - 已點擊右鍵選單的「複製」選項")
        page.wait_for_timeout(500)
        
        # ===== 3. 拖曳操作 =====
        print("\n" + "=" * 50)
        print("3. 拖曳操作")
        print("=" * 50)
        
        # 方法1：使用 drag_and_drop
        page.drag_and_drop("#dragItem", "#dropZone")
        print("   - 已將元素從來源區拖曳到目標區")
        page.wait_for_timeout(1000)
        
        # 拖回來源區
        page.drag_and_drop("#dragItem", "#sourceZone")
        print("   - 已將元素拖回來源區")
        page.wait_for_timeout(500)
        
        # 方法2：手動控制拖曳
        print("   - 使用手動控制方式再次拖曳...")
        page.hover("#dragItem")
        page.mouse.down()
        page.hover("#dropZone")
        page.mouse.up()
        print("   - 手動拖曳完成")
        page.wait_for_timeout(1000)
        
        # ===== 4. 鍵盤操作 =====
        print("\n" + "=" * 50)
        print("4. 鍵盤操作")
        print("=" * 50)
        
        # 點擊輸入框並輸入文字
        page.click("#textInput")
        page.keyboard.type("Hello Playwright!", delay=100)
        print("   - 已在文字輸入框中輸入 'Hello Playwright!'")
        page.wait_for_timeout(500)
        
        # 使用組合鍵全選
        page.keyboard.press("Control+A")
        print("   - 已使用 Ctrl+A 全選文字")
        page.wait_for_timeout(300)
        
        # 複製文字
        page.keyboard.press("Control+C")
        print("   - 已使用 Ctrl+C 複製文字")
        page.wait_for_timeout(300)
        
        # 在搜尋框中輸入並按 Enter
        page.click("#searchInput")
        page.keyboard.type("Playwright 教學", delay=80)
        print("   - 已在搜尋框中輸入 'Playwright 教學'")
        page.wait_for_timeout(300)
        
        page.keyboard.press("Enter")
        print("   - 已按下 Enter 鍵執行搜尋")
        page.wait_for_timeout(1000)
        
        # ===== 5. 滾動操作 =====
        print("\n" + "=" * 50)
        print("5. 滾動操作")
        print("=" * 50)
        
        # 滾動容器內的元素
        page.click("#scrollToTarget")
        print("   - 已點擊「滾動到目標」按鈕")
        page.wait_for_timeout(1000)
        
        page.click("#scrollToBottom")
        print("   - 已點擊「滾動到底部」按鈕")
        page.wait_for_timeout(500)
        
        page.click("#scrollToTop")
        print("   - 已點擊「回到頂部」按鈕")
        page.wait_for_timeout(500)
        
        # 滾動整個頁面到底部
        print("   - 滾動整個頁面到底部...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        
        # 使用 scroll_into_view_if_needed 滾動到元素
        page.locator("#bottomButton").scroll_into_view_if_needed()
        print("   - 已滾動到底部按鈕位置")
        page.wait_for_timeout(500)
        
        # 點擊底部按鈕確認到達
        page.click("#bottomButton")
        print("   - 已點擊「確認到達底部」按鈕")
        page.wait_for_timeout(1000)
        
        # 滾動回頁面頂部
        page.evaluate("window.scrollTo(0, 0)")
        print("   - 已滾動回頁面頂部")
        page.wait_for_timeout(500)
        
        # ===== 完成 =====
        print("\n" + "=" * 50)
        print("✅ 所有進階互動操作已完成！")
        print("=" * 50)
        
        # 等待一下讓使用者觀察結果
        page.wait_for_timeout(3000)
        
        # 關閉瀏覽器
        browser.close()
        print("\n瀏覽器已關閉")


if __name__ == "__main__":
    interactive_example()
