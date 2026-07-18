from playwright.sync_api import sync_playwright
import os

# 定義主要函式，接收 headless（無頭模式）與 slow_mo（操作延遲）參數
def jls_extract_def(headless, slow_mo):
    # 使用 with 語句建立 Playwright 實例，結束時自動釋放資源
    with sync_playwright() as p:
        # 啟動瀏覽器（有頭模式），並設定每次操作延遲 500 毫秒
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        # 開啟新分頁
        page = browser.new_page()
    
        # 取得當前檔案的絕對路徑
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 拼接出本機 HTML 表單檔案的完整路徑
        html_file = os.path.join(current_dir, "form_demo.html")
    
        # 使用 file:// 協定訪問本機 HTML 檔案
        page.goto(f"file://{html_file}")
    
        # === 表單操作示範 ===
        # 1. 填寫文字欄位：姓名
        page.fill("input#name", "張三")
        # 2. 填寫文字欄位：電子郵件
        page.fill("input#email", "zhang@example.com")
        # 3. 選擇下拉選單：國家
        page.select_option("select#country", "Taiwan")
        # 4. 勾選核取方塊：訂閱
        page.check("input#subscribe")
    
        # 點擊提交按鈕
        page.click("button#submit")
    
        # 等待網路請求全部完成（確保提交後的頁面已載入完畢）
        page.wait_for_load_state("networkidle")
    
        # 停留 2 秒，讓使用者能看到結果
        page.wait_for_timeout(2000)
    
        # 關閉瀏覽器
        browser.close()
    return html_file


def basic_operations():
    # 呼叫主要函式，設定有頭模式（看得到瀏覽器）、操作延遲 500ms
    html_file = jls_extract_def(headless=False, slow_mo=500)

if __name__ == "__main__":
    basic_operations()
