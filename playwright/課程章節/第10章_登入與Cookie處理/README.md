# 第十章：登入與 Cookie 處理

學習如何處理需要登入的網站和管理 Cookie。

## 📁 本章檔案

- **[`login_example.py`](./login_example.py)** - 登入與 Cookie 處理範例程式
- **[`login_demo.html`](./login_demo.html)** - 登入功能測試頁面
- **`README.md`** - 本章教學文件

## 🚀 快速開始

```bash
# 執行示範程式
python login_example.py
```

程式會自動開啟 `login_demo.html` 並展示登入、Cookie 儲存和載入的功能。Cookie 和瀏覽器狀態會儲存在 `output/` 目錄中。

**測試帳號：**
- 用戶名：`admin`
- 密碼：`password123`

## 10.1 自動登入

### 填寫登入表單
```python
from playwright.sync_api import sync_playwright

def auto_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 訪問登入頁面
        page.goto("https://example.com/login")
        
        # 填寫帳號密碼
        page.fill("input#username", "your_username")
        page.fill("input#password", "your_password")
        
        # 點擊登入按鈕
        page.click("button#login")
        
        # 等待登入完成
        page.wait_for_url("**/dashboard")
        print("登入成功！")
        
        # 在登入後的頁面操作
        page.click("a#profile")
        
        browser.close()
```

### 處理驗證碼（手動介入）
```python
def login_with_captcha():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://example.com/login")
        page.fill("input#username", "username")
        page.fill("input#password", "password")
        
        # 等待用戶手動輸入驗證碼
        print("請手動輸入驗證碼...")
        page.wait_for_timeout(30000)  # 等待 30 秒
        
        # 或等待特定元素出現（表示登入成功）
        page.wait_for_selector("#user-dashboard", timeout=60000)
        
        print("已登入")
        browser.close()
```

---

## 10.2 Cookie 管理

### 儲存 Cookie
```python
import json

def save_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 登入
        page.goto("https://example.com/login")
        page.fill("input#username", "username")
        page.fill("input#password", "password")
        page.click("button#login")
        page.wait_for_load_state("networkidle")
        
        # 取得 Cookie
        cookies = context.cookies()
        
        # 儲存 Cookie
        with open("cookies.json", "w") as f:
            json.dump(cookies, f, indent=2)
        
        print("Cookie ��儲存")
        
        context.close()
        browser.close()
```

### 載入已儲存的 Cookie
```python
def load_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 載入 Cookie
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        
        # 建立帶有 Cookie 的 context
        context = browser.new_context()
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        # 直接訪問需登入的頁面（已有 Cookie）
        page.goto("https://example.com/dashboard")
        
        print("使用已儲存的 Cookie 登入成功")
        
        context.close()
        browser.close()
```

### 保持登入狀態
```python
def stay_logged_in():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 嘗試載入 Cookie
        try:
            with open("cookies.json", "r") as f:
                cookies = json.load(f)
            context = browser.new_context()
            context.add_cookies(cookies)
            print("使用已儲存的 Cookie")
        except FileNotFoundError:
            # Cookie 不存在，需要登入
            context = browser.new_context()
            page = context.new_page()
            
            # 執行登入
            page.goto("https://example.com/login")
            page.fill("input#username", "username")
            page.fill("input#password", "password")
            page.click("button#login")
            page.wait_for_load_state("networkidle")
            
            # 儲存 Cookie
            cookies = context.cookies()
            with open("cookies.json", "w") as f:
                json.dump(cookies, f)
            print("已登入並儲存 Cookie")
        
        page = context.new_page()
        page.goto("https://example.com/dashboard")
        
        # 執行需要登入的操作
        print(page.title())
        
        context.close()
        browser.close()
```

---

## 10.3 Session 保存

### 儲存瀏覽器上下文
```python
def save_browser_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 建立持久化 context
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()
        
        # 登入
        page.goto("https://example.com/login")
        page.fill("input#username", "username")
        page.fill("input#password", "password")
        page.click("button#login")
        page.wait_for_load_state("networkidle")
        
        # 儲存狀態（包含 Cookie、localStorage 等）
        context.storage_state(path="state.json")
        print("瀏覽器狀態已儲存")
        
        context.close()
        browser.close()
```

### 重複使用登入狀態
```python
def reuse_login_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 載入儲存的狀態
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()
        
        # 直接訪問需登入的頁面
        page.goto("https://example.com/dashboard")
        print("已使用儲存的登入狀態")
        
        context.close()
        browser.close()
```

---

## 完整範例：登入並爬取會員資料

```python
from playwright.sync_api import sync_playwright
import json
import os

def scrape_member_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 檢查是否有儲存的狀態
        if os.path.exists("auth_state.json"):
            context = browser.new_context(storage_state="auth_state.json")
            print("使用已儲存的登入狀態")
        else:
            context = browser.new_context()
            page = context.new_page()
            
            # 執行登入
            page.goto("https://example.com/login")
            page.fill("input[name='username']", "your_username")
            page.fill("input[name='password']", "your_password")
            page.click("button[type='submit']")
            page.wait_for_url("**/dashboard")
            
            # 儲存登入狀態
            context.storage_state(path="auth_state.json")
            print("登入成功並儲存狀態")
        
        page = context.new_page()
        
        # 訪問會員頁面
        page.goto("https://example.com/member/profile")
        page.wait_for_selector("#profile-data")
        
        # 擷取資料
        member_data = {
            "name": page.locator("#name").inner_text(),
            "email": page.locator("#email").inner_text(),
            "points": page.locator("#points").inner_text()
        }
        
        # 訪問訂單頁面
        page.goto("https://example.com/member/orders")
        page.wait_for_selector(".order-item")
        
        orders = []
        for order in page.locator(".order-item").all():
            orders.append({
                "id": order.locator(".order-id").inner_text(),
                "date": order.locator(".order-date").inner_text(),
                "total": order.locator(".order-total").inner_text()
            })
        
        member_data["orders"] = orders
        
        # 儲存資料
        with open("member_data.json", "w", encoding="utf-8") as f:
            json.dump(member_data, f, ensure_ascii=False, indent=2)
        
        print(f"擷取完成：{len(orders)} 筆訂單")
        
        context.close()
        browser.close()

if __name__ == "__main__":
    scrape_member_data()
```

---

## 安全提醒

1. **不要將帳號密碼寫死在程式碼中**
2. **使用環境變數或設定檔**
3. **不要將 Cookie 或 state.json 上傳到 Git**
4. **定期更新 Cookie（會過期）**

### 使用環境變數
```python
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("LOGIN_USERNAME")
password = os.getenv("LOGIN_PASSWORD")
```

---

## 🌐 真實網站範例：PTT 年齡確認 Cookie

示範如何通過 PTT 的年齡確認頁面，儲存 Cookie 並在下次訪問時重複使用。

```python
from playwright.sync_api import sync_playwright
import json
from pathlib import Path

out_dir = Path("output")
out_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    print("=== 第一次訪問：通過年齡確認並儲存 Cookie ===")
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)
    print(f"已進入看板，文章數量: {page.locator('div.title a').count()}")

    cookies = context.cookies()
    with open(out_dir / "ptt_cookies.json", "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"已儲存 {len(cookies)} 個 Cookie")
    context.close()

    print("\n=== 第二次訪問：載入 Cookie，跳過年齡確認 ===")
    with open(out_dir / "ptt_cookies.json", "r") as f:
        saved_cookies = json.load(f)

    context2 = browser.new_context()
    context2.add_cookies(saved_cookies)
    page2 = context2.new_page()
    page2.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page2.wait_for_load_state("domcontentloaded")

    current_url = page2.url
    print(f"當前網址: {current_url}")
    if "over18" not in current_url:
        print("成功！已跳過年齡確認頁面，直接進入看板")
    else:
        print("Cookie 未生效，需要重新確認年齡")

    context2.close()
    browser.close()
```

**執行方式：**
```bash
uv run python playwright/課程章節/第10章_登入與Cookie處理/real_example.py
```

---

## 練習題

1. 實作自動登入並儲存 Cookie
2. 使用儲存的 Cookie 重複登入
3. 爬取需要登入才能看到的資料
4. 實作完整的會員資料爬取程式

## 本章實戰

[專案 10：登入狀態保存 →](../../實戰專案/專案10_登入狀態保存/README.md)

---

[← 上一章：網路請求與回應](../第09章_網路請求與回應/README.md) | [返回目錄](../../README.md) | [下一章：反爬蟲對策 →](../第11章_反爬蟲對策/README.md)
