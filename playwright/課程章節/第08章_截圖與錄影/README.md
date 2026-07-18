# 第八章：截圖與錄影

學習如何擷取網頁畫面和錄製操作過程。

## 📁 本章檔案

- **[`screenshot_example.py`](./screenshot_example.py)** - 截圖與錄影範例程式
- **[`screenshot_demo.html`](./screenshot_demo.html)** - 截圖測試頁面
- **`README.md`** - 本章教學文件

## 🚀 快速開始

```bash
# 執行示範程式
python screenshot_example.py
```

程式會自動開啟 `screenshot_demo.html` 並展示各種截圖和錄影功能。截圖檔案將儲存於 `output/` 目錄中。

## 8.1 頁面截圖

### 全頁面截圖
```python
# 截取整個頁面
page.screenshot(path="screenshot.png")

# 全頁面截圖（包含需滾動的部分）
page.screenshot(path="full_page.png", full_page=True)
```

### 元素截圖
```python
# 截取特定元素
element = page.locator("#content")
element.screenshot(path="element.png")

# 截取多個元素
for i, item in enumerate(page.locator(".item").all()):
    item.screenshot(path=f"item_{i}.png")
```

### 自訂截圖區域
```python
# 指定尺寸
page.set_viewport_size({"width": 1920, "height": 1080})
page.screenshot(path="custom_size.png")

# 裁剪特定區域
page.screenshot(
    path="clip.png",
    clip={"x": 0, "y": 0, "width": 800, "height": 600}
)

# 高品質截圖
page.screenshot(
    path="high_quality.png",
    type="png",  # 或 "jpeg"
    quality=100  # 只對 jpeg 有效
)
```

---

## 8.2 錄製操作影片

### 開始錄影
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 開始錄影
    context = browser.new_context(
        record_video_dir="videos/",
        record_video_size={"width": 1280, "height": 720"}
    )
    
    page = context.new_page()
    page.goto("https://example.com")
    page.click("button")
    
    # 關閉以儲存影片
    context.close()
    browser.close()
```

### 停止並儲存影片
```python
def record_video():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 設定錄影
        context = browser.new_context(
            record_video_dir="recordings/",
            record_video_size={"width": 1920, "height": 1080"}
        )
        
        page = context.new_page()
        
        # 執行操作
        page.goto("https://example.com")
        page.fill("input#search", "Playwright")
        page.click("button#submit")
        page.wait_for_load_state("networkidle")
        
        # 取得影片路徑
        video_path = page.video.path()
        
        # 關閉以完成錄影
        page.close()
        context.close()
        browser.close()
        
        print(f"影片已儲存: {video_path}")
```

---

## 8.3 生成 PDF

### 將網頁儲存為 PDF
```python
# 基本 PDF 生成
page.goto("https://example.com")
page.pdf(path="page.pdf")

# 完整頁面 PDF
page.pdf(
    path="full_page.pdf",
    format="A4",
    print_background=True
)
```

### PDF 格式設定
```python
page.pdf(
    path="custom.pdf",
    format="A4",  # 或 "Letter", "Legal", "A3" 等
    landscape=False,  # 橫向/直向
    margin={
        "top": "1cm",
        "right": "1cm",
        "bottom": "1cm",
        "left": "1cm"
    },
    print_background=True,  # 列印背景顏色
    prefer_css_page_size=False
)

# 自訂尺寸
page.pdf(
    path="custom_size.pdf",
    width="210mm",
    height="297mm"
)
```

---

## 完整範例

```python
from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def capture_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 設定錄影
        context = browser.new_context(
            record_video_dir="videos/",
            viewport={"width": 1920, "height": 1080"}
        )
        
        page = context.new_page()
        
        # 訪問網站
        page.goto("https://example.com")
        page.wait_for_load_state("networkidle")
        
        # 建立輸出目錄
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("output", exist_ok=True)
        
        # 全頁面截圖
        page.screenshot(
            path=f"output/full_page_{timestamp}.png",
            full_page=True
        )
        
        # 元素截圖
        page.locator("#main-content").screenshot(
            path=f"output/content_{timestamp}.png"
        )
        
        # 生成 PDF
        page.pdf(
            path=f"output/page_{timestamp}.pdf",
            format="A4",
            print_background=True
        )
        
        # 關閉並取得影片
        video_path = page.video.path()
        
        page.close()
        context.close()
        browser.close()
        
        print(f"截圖、PDF 和影片已儲存")
        print(f"影片路徑: {video_path}")

if __name__ == "__main__":
    capture_page()
```

---

## 實用技巧

### 批量截圖
```python
def batch_screenshot(urls):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        for i, url in enumerate(urls):
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=f"screenshot_{i}.png", full_page=True)
            print(f"已截圖: {url}")
        
        browser.close()

urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net"
]
batch_screenshot(urls)
```

### 比較截圖（視覺回歸測試）
```python
import os

def visual_regression_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://example.com")
        
        # 第一次截圖（基準）
        if not os.path.exists("baseline.png"):
            page.screenshot(path="baseline.png")
            print("基準截圖已建立")
        else:
            # 新的截圖
            page.screenshot(path="current.png")
            print("請手動比較 baseline.png 和 current.png")
        
        browser.close()
```

---

## 🌐 真實網站範例：維基百科截圖

在維基百科臺灣條目上示範全頁截圖、元素截圖和資訊框截圖。

```python
from playwright.sync_api import sync_playwright
from pathlib import Path

out_dir = Path("output")
out_dir.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("=== 全頁截圖 ===")
    page.goto("https://zh.wikipedia.org/wiki/臺灣", timeout=15000)
    page.wait_for_load_state("domcontentloaded")
    page.screenshot(path=str(out_dir / "wikipedia_full.png"), full_page=True)
    print("已儲存: wikipedia_full.png")

    print("\n=== 元素截圖 ===")
    heading = page.locator("#firstHeading")
    heading.screenshot(path=str(out_dir / "heading.png"))
    print(f"已儲存: heading.png ({heading.inner_text()})")

    print("\n=== 資訊框截圖 ===")
    info_box = page.locator("table.infobox").first
    info_box.screenshot(path=str(out_dir / "infobox.png"))
    print("已儲存: infobox.png")

    browser.close()
```

**執行方式：**
```bash
uv run python playwright/課程章節/第08章_截圖與錄影/real_example.py
```

---

## 練習題

1. 截取你常用網站的首頁（全頁面截圖）
2. 錄製一個完整的表單填寫過程
3. 將一篇網路文章儲存為 PDF
4. 批量截取多個網站的截圖

## 本章實戰

[專案 08：網頁存證報告 →](../../實戰專案/專案08_網頁存證報告/README.md)

---

[← 上一章：多頁面與框架處理](../第07章_多頁面與框架處理/README.md) | [返回目錄](../../README.md) | [下一章：網路請求與回應 →](../第09章_網路請求與回應/README.md)
