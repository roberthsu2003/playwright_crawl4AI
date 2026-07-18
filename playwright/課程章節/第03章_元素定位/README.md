# 第三章：元素定位(Locator)

元素定位是網頁自動化的核心技能。本章將學習多種定位元素的方法。

## 📁 本章檔案

- **[`index.py`](./index.py)** - 元素定位示範程式（建議先執行這個）
- **[`login_demo.html`](./login_demo.html)** - 練習用的登入頁面
- **`README.md`** - 本章教學文件

## 🚀 快速開始

```bash
# 執行示範程式
python index.py
```

程式會自動開啟 `login_demo.html` 並展示四種不同的元素定位方法。

## 3.1 CSS 選擇器

### 基本 CSS 選擇器語法

```python
# 標籤選擇器
page.click("button")

# ID 選擇器
page.click("#submit-btn")

# 類別選擇器
page.click(".primary-button")

# 屬性選擇器
page.click("[data-test='login-button']")

# 組合選擇器
page.click("form#login button.submit")
```

### 常用 CSS 選擇器

| 選擇器 | 說明 | 範例 |
|--------|------|------|
| `element` | 標籤名稱(tag selector) | `button`, `input` |
| `#id` | ID 選擇器(id selector) | `#submit` |
| `.class` | 類別選擇器(class selector) | `.btn-primary` |
| `[attr]` | 屬性選擇器(attribute Selector) | `[type='submit']` |
| `parent > child` | 直接子元素(child selector) | `form > button` |
| `ancestor descendant` | 後代元素(descendant selector) | `div button` |
| `element:nth-child(n)` | 第 n 個子元素(nth-child selector) | `li:nth-child(2)` |

---

## 3.2 XPath 定位

### XPath 基礎語法

```python
# 絕對路徑（不建議）
page.click("xpath=/html/body/div/button")

# 相對路徑
page.click("xpath=//button[@id='submit']")

# 文字匹配
page.click("xpath=//button[text()='登入']")

# 包含文字
page.click("xpath=//button[contains(text(), '提交')]")
```

### 常用 XPath 表達式

```python
# 根據屬性
"xpath=//input[@name='username']"

# 根據文字
"xpath=//a[text()='首頁']"

# 包含文字
"xpath=//div[contains(text(), '歡迎')]"

# 父子關係
"xpath=//form[@id='login']//input[@type='password']"

# 同級元素
"xpath=//label[text()='姓名']/following-sibling::input"
```

---

## 3.3 Playwright 內建定位器

Playwright 提供了更語義化的定位器，**建議優先使用**。

### `get_by_text()` - 根據文字定位

```python
# 精確匹配
page.get_by_text("登入").click()

# 部分匹配
page.get_by_text("登入", exact=False).click()
```

### `get_by_role()` - 根據角色定位

```python
# 點擊按鈕
page.get_by_role("button", name="提交").click()

# 點擊連結
page.get_by_role("link", name="首頁").click()

# 填寫文字框
page.get_by_role("textbox", name="用戶名").fill("admin")
```

**常用角色：**
- `button` - 按鈕
- `link` - 連結
- `textbox` - 文字框
- `checkbox` - 核取方塊
- `radio` - 單選按鈕
- `heading` - 標題

### `get_by_label()` - 根據標籤定位

```python
# 根據 label 文字
page.get_by_label("用戶名").fill("admin")
page.get_by_label("密碼").fill("password123")
```

### `get_by_placeholder()` - 根據提示文字定位

```python
page.get_by_placeholder("請輸入Email").fill("user@example.com")
page.get_by_placeholder("搜尋...").fill("Playwright")
```

### `get_by_test_id()` - 根據測試 ID 定位

```python
# HTML: <button data-testid="submit-btn">提交</button>
page.get_by_test_id("submit-btn").click()
```

---

## 3.4 定位策略最佳實踐

### 優先順序建議（由高到低）

1. **`get_by_role()`** - 最具語義，最穩定
2. **`get_by_label()`** - 適合表單元素
3. **`get_by_placeholder()`** - 適合輸入框
4. **`get_by_text()`** - 適合文字內容
5. **`get_by_test_id()`** - 需要在 HTML 中添加
6. **CSS 選擇器** - 靈活但可能不穩定
7. **XPath** - 最後選擇

### 如何處理動態元素

```python
# 使用部分匹配
page.locator("text=/產品.*/").click()

# 使用包含屬性
page.locator("[class*='btn-']").click()

# 組合定位
page.locator("form").get_by_role("button", name="提交").click()

# 鏈式定位
page.locator("div.container").locator("button.submit").click()
```

---

## 完整範例

### 執行 index.py

本章提供了完整的示範程式 `index.py`，展示四種元素定位方法：

```bash
python index.py
```

**執行結果：**
```
============================================================
Playwright 元素定位示範
============================================================
✓ 已開啟登入頁面

使用 get_by_label() 定位輸入欄位...
✓ 已填入用戶名：admin
✓ 已填入密碼：password

使用 get_by_role() 定位按鈕...
✓ 已點擊登入按鈕

✓ 登入成功！

程式執行完成，3 秒後關閉瀏覽器...

============================================================
示範完成！
============================================================
```

### 程式碼說明

`index.py` 的核心程式碼：

```python
from playwright.sync_api import sync_playwright
import os

def element_location_demo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 開啟本地 HTML 檔案
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = os.path.join(current_dir, "login_demo.html")
        page.goto(f"file://{html_file}")
        
        # 方法1：使用 get_by_label() - 根據 label 文字定位
        page.get_by_label("用戶名").fill("admin")
        page.get_by_label("密碼").fill("password")
        
        # 方法2：使用 get_by_role() - 根據元素角色定位
        page.get_by_role("button", name="登入").click()
        
        # 方法3：使用 CSS 選擇器（已註解）
        # page.locator("#username").fill("admin")
        # page.locator("#password").fill("password")
        # page.locator("#login-button").click()
        
        # 方法4：使用 XPath（已註解）
        # page.locator("xpath=//input[@id='username']").fill("admin")
        # page.locator("xpath=//input[@id='password']").fill("password")
        # page.locator("xpath=//button[text()='登入']").click()
        
        page.wait_for_timeout(3000)
        browser.close()
```

### login_demo.html 說明

這是一個完整的登入頁面，包含：
- 用戶名輸入框（帶有 `<label>` 標籤）
- 密碼輸入框（帶有 `<label>` 標籤）
- 登入按鈕（帶有 `role="button"` 屬性）
- 登入成功的動畫提示
- 測試帳號資訊提示

**測試帳號：**
- 用戶名：`admin`
- 密碼：`password`

你可以直接在瀏覽器中開啟 `login_demo.html` 查看頁面效果。

---

## 🌐 真實網站範例：PTT 文章定位

使用四種不同的元素定位技巧，在 PTT 八卦版上擷取文章資訊。

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.ptt.cc/bbs/Gossiping/index.html")
    page.wait_for_selector("button.btn-big", timeout=10000)
    page.get_by_role("button", name="我同意，我已年滿十八歲").click()
    page.wait_for_selector("div.r-ent", timeout=10000)

    print("=== CSS 選擇器 ===")
    titles = page.locator("div.title a").all()
    for t in titles[:3]:
        print(f"  {t.inner_text()}")

    print("\n=== get_by_role ===")
    links = page.get_by_role("link").all()
    for link in links[:5]:
        text = link.inner_text().strip()
        if text:
            print(f"  {text}")

    print("\n=== XPath ===")
    xpath_titles = page.locator("//div[@class='title']/a").all()
    for t in xpath_titles[:3]:
        print(f"  {t.inner_text()}")

    print("\n=== 取得連結屬性 ===")
    for t in titles[:3]:
        href = t.get_attribute("href")
        print(f"  {t.inner_text()} -> {href}")

    browser.close()
```

**執行方式：**
```bash
uv run python playwright/課程章節/第03章_元素定位/real_example.py
```

---

## 練習題

1. **修改 index.py**：取消註解其他定位方法（CSS 選擇器、XPath），測試不同的定位方式
2. **使用 3 種不同方法**定位 `login_demo.html` 中的登入按鈕
3. **嘗試所有內建定位器**（get_by_*）在 `login_demo.html` 上
4. **開啟開發者工具**（F12）查看 `login_demo.html` 的元素結構，練習寫 CSS 選擇器
5. **修改 login_demo.html**：加入更多表單元素（如：Email、電話），並用 Playwright 操作它們

## 本章實戰

[專案 03：購物網站元素定位 →](../../實戰專案/專案03_購物網站元素定位/README.md)

---

[← 上一章：基礎操作](../第02章_基礎操作/README.md) | [返回目錄](../../README.md) | [下一章：等待與同步 →](../第04章_等待與同步/README.md)
