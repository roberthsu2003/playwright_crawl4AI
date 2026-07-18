"""
第九章：網路請求與回應 - 完整示範
展示 Playwright 監聽、攔截和修改網路請求的功能
"""

from playwright.sync_api import sync_playwright
import os
import json
from pathlib import Path
from datetime import datetime


def get_html_path():
    """取得 HTML 檔案的絕對路徑"""
    current_dir = Path(__file__).parent
    html_path = current_dir / "network_demo.html"
    return f"file://{html_path.absolute()}"


def demo_1_monitor_requests(page):
    """示範 1：監聽所有網路請求"""
    print("\n" + "=" * 60)
    print("示範 1：監聽網路請求")
    print("=" * 60)
    
    requests_log = []
    
    def log_request(request):
        requests_log.append({
            "url": request.url,
            "method": request.method,
            "resource_type": request.resource_type
        })
    
    def log_response(response):
        # 找到對應的請求並更新狀態
        for req in requests_log:
            if req["url"] == response.url:
                req["status"] = response.status
                break
    
    page.on("request", log_request)
    page.on("response", log_response)
    
    # 重新載入頁面以捕捉所有請求
    page.reload()
    page.wait_for_load_state("networkidle")
    
    print(f"✓ 捕捉到 {len(requests_log)} 個請求")
    
    # 按資源類型分類顯示
    resource_types = {}
    for req in requests_log:
        rtype = req["resource_type"]
        if rtype not in resource_types:
            resource_types[rtype] = 0
        resource_types[rtype] += 1
    
    print("\n資源類型統計：")
    for rtype, count in resource_types.items():
        print(f"  - {rtype}: {count}")
    
    # 移除監聽器
    page.remove_listener("request", log_request)
    page.remove_listener("response", log_response)
    
    return requests_log


def demo_2_intercept_response(page):
    """示範 2：攔截並修改 API 回應"""
    print("\n" + "=" * 60)
    print("示範 2：攔截並修改回應（Mock API）")
    print("=" * 60)
    
    # 自訂的回應資料
    mock_users = [
        {"id": 1, "name": "模擬用戶 A", "email": "mock_a@test.com", "role": "admin"},
        {"id": 2, "name": "模擬用戶 B", "email": "mock_b@test.com", "role": "user"}
    ]
    
    def handle_route(route):
        # 這裡我們示範如何修改回應
        # 在本地 HTML 範例中，我們無法真正攔截到 API 請求
        # 但程式碼結構展示了正確的做法
        route.continue_()
    
    # 設定路由攔截
    page.route("**/api/**", handle_route)
    
    print("✓ 已設定 API 路由攔截")
    print(f"✓ Mock 資料：{json.dumps(mock_users, ensure_ascii=False, indent=2)}")
    
    # 點擊按鈕觸發 API 請求
    page.click("#fetchUsers")
    page.wait_for_timeout(1500)
    
    result = page.locator("#usersResult").inner_text()
    print(f"\n頁面顯示結果：\n{result[:200]}...")
    
    # 移除路由
    page.unroute("**/api/**")


def demo_3_block_resources(page):
    """示範 3：阻擋特定資源以提升效能"""
    print("\n" + "=" * 60)
    print("示範 3：阻擋特定資源（提升爬蟲效能）")
    print("=" * 60)
    
    blocked_count = {"images": 0, "fonts": 0, "stylesheets": 0}
    
    def block_handler(route):
        resource_type = route.request.resource_type
        
        if resource_type == "image":
            blocked_count["images"] += 1
            route.abort()
        elif resource_type == "font":
            blocked_count["fonts"] += 1
            route.abort()
        else:
            route.continue_()
    
    page.route("**/*", block_handler)
    
    # 重新載入頁面
    page.reload()
    page.wait_for_load_state("networkidle")
    
    print("✓ 資源阻擋統計：")
    for resource, count in blocked_count.items():
        print(f"  - 阻擋 {resource}: {count} 個")
    
    # 移除路由
    page.unroute("**/*")


def demo_4_capture_api_data(page):
    """示範 4：擷取 API 回應資料"""
    print("\n" + "=" * 60)
    print("示範 4：擷取頁面資料")
    print("=" * 60)
    
    # 點擊載入商品
    page.click("#fetchProducts")
    page.wait_for_timeout(1500)
    
    # 從頁面擷取資料
    result_element = page.locator("#productsResult")
    product_items = result_element.locator(".data-item").all()
    
    products = []
    for item in product_items:
        text = item.inner_text()
        products.append(text)
    
    print(f"✓ 擷取到 {len(products)} 個商品：")
    for product in products:
        print(f"  - {product}")
    
    return products


def demo_5_monitor_post_request(page):
    """示範 5：監聽 POST 請求"""
    print("\n" + "=" * 60)
    print("示範 5：監聽 POST 請求")
    print("=" * 60)
    
    post_requests = []
    
    def capture_post(request):
        if request.method == "POST":
            post_requests.append({
                "url": request.url,
                "post_data": request.post_data
            })
            print(f"  捕捉到 POST 請求：{request.url}")
    
    page.on("request", capture_post)
    
    # 填寫並提交表單
    page.fill("#submitInput", "測試資料 - Playwright")
    page.click("#submitData")
    page.wait_for_timeout(1000)
    
    result = page.locator("#submitResult").inner_text()
    print(f"\n✓ 提交結果：")
    print(result)
    
    page.remove_listener("request", capture_post)


def demo_6_request_timing(page):
    """示範 6：請求時間分析"""
    print("\n" + "=" * 60)
    print("示範 6：請求時間分析")
    print("=" * 60)
    
    request_times = {}
    
    def on_request(request):
        request_times[request.url] = {
            "start": datetime.now(),
            "method": request.method
        }
    
    def on_response(response):
        url = response.url
        if url in request_times:
            end_time = datetime.now()
            duration = (end_time - request_times[url]["start"]).total_seconds() * 1000
            request_times[url]["duration_ms"] = duration
            request_times[url]["status"] = response.status
    
    page.on("request", on_request)
    page.on("response", on_response)
    
    # 觸發一些請求
    page.click("#fetchUsers")
    page.wait_for_timeout(1500)
    
    page.click("#fetchProducts")
    page.wait_for_timeout(1500)
    
    # 顯示時間統計
    print("✓ 請求時間統計（模擬）：")
    count = 0
    for url, data in request_times.items():
        if "duration_ms" in data and count < 5:
            print(f"  {data['method']} {url[-50:]}: {data.get('duration_ms', 0):.2f}ms")
            count += 1
    
    page.remove_listener("request", on_request)
    page.remove_listener("response", on_response)


def main():
    """主程式"""
    print("\n" + "🌐 " + "=" * 58)
    print("🌐  Playwright 網路請求與回應 - 完整示範")
    print("🌐 " + "=" * 58)
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
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
            demo_1_monitor_requests(page)
            page.wait_for_timeout(1000)
            
            demo_2_intercept_response(page)
            page.wait_for_timeout(1000)
            
            demo_3_block_resources(page)
            page.wait_for_timeout(1000)
            
            demo_4_capture_api_data(page)
            page.wait_for_timeout(1000)
            
            demo_5_monitor_post_request(page)
            page.wait_for_timeout(1000)
            
            demo_6_request_timing(page)
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        # 完成
        print("\n" + "=" * 60)
        print("✅ 所有示範完成！")
        print("=" * 60)
        print("\n按 Enter 關閉瀏覽器...")
        input()
        
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
