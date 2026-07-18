"""
第八章：截圖與錄影 - 完整示範
展示 Playwright 的截圖、錄影和 PDF 生成功能
"""

from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from pathlib import Path


def get_html_path():
    """取得 HTML 檔案的絕對路徑"""
    current_dir = Path(__file__).parent
    html_path = current_dir / "screenshot_demo.html"
    return f"file://{html_path.absolute()}"


def create_output_dir():
    """建立輸出目錄"""
    current_dir = Path(__file__).parent
    output_dir = current_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def demo_1_basic_screenshot(page, output_dir):
    """示範 1：基本截圖"""
    print("\n" + "=" * 60)
    print("示範 1：基本截圖")
    print("=" * 60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 視窗截圖（當前可見範圍）
    viewport_path = output_dir / f"viewport_{timestamp}.png"
    page.screenshot(path=str(viewport_path))
    print(f"✓ 視窗截圖已儲存：{viewport_path.name}")
    
    # 全頁面截圖
    fullpage_path = output_dir / f"fullpage_{timestamp}.png"
    page.screenshot(path=str(fullpage_path), full_page=True)
    print(f"✓ 全頁截圖已儲存：{fullpage_path.name}")


def demo_2_element_screenshot(page, output_dir):
    """示範 2：元素截圖"""
    print("\n" + "=" * 60)
    print("示範 2：元素截圖")
    print("=" * 60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 截取特定元素
    element_path = output_dir / f"element_{timestamp}.png"
    page.locator("#elementToCapture").screenshot(path=str(element_path))
    print(f"✓ 特定元素截圖已儲存：{element_path.name}")
    
    # 截取統計數據區
    stats_path = output_dir / f"stats_{timestamp}.png"
    page.locator(".stats-container").screenshot(path=str(stats_path))
    print(f"✓ 統計數據截圖已儲存：{stats_path.name}")
    
    # 截取多個卡片
    cards = page.locator(".card").all()
    print(f"✓ 找到 {len(cards)} 個卡片元素")
    
    for i, card in enumerate(cards[:2]):  # 只截取前 2 個
        card_path = output_dir / f"card_{i+1}_{timestamp}.png"
        card.screenshot(path=str(card_path))
        print(f"  - 卡片 {i+1} 已截圖：{card_path.name}")


def demo_3_custom_screenshot(page, output_dir):
    """示範 3：自訂截圖設定"""
    print("\n" + "=" * 60)
    print("示範 3：自訂截圖設定")
    print("=" * 60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JPEG 格式截圖
    jpeg_path = output_dir / f"page_{timestamp}.jpg"
    page.screenshot(
        path=str(jpeg_path),
        type="jpeg",
        quality=80
    )
    print(f"✓ JPEG 截圖已儲存：{jpeg_path.name}")
    
    # 裁剪特定區域
    clip_path = output_dir / f"clip_{timestamp}.png"
    page.screenshot(
        path=str(clip_path),
        clip={
            "x": 0,
            "y": 0,
            "width": 800,
            "height": 400
        }
    )
    print(f"✓ 裁剪區域截圖已儲存：{clip_path.name}")


def demo_4_screenshot_with_actions(page, output_dir):
    """示範 4：操作前後截圖對比"""
    print("\n" + "=" * 60)
    print("示範 4：操作前後截圖對比")
    print("=" * 60)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 操作前截圖
    before_path = output_dir / f"before_action_{timestamp}.png"
    page.locator(".content-section").last.screenshot(path=str(before_path))
    print(f"✓ 操作前截圖：{before_path.name}")
    
    # 執行操作
    page.click("#actionBtn1")
    page.wait_for_timeout(500)
    print("✓ 已點擊動作按鈕 1")
    
    # 操作後截圖
    after_path = output_dir / f"after_action_{timestamp}.png"
    page.locator(".content-section").last.screenshot(path=str(after_path))
    print(f"✓ 操作後截圖：{after_path.name}")


def demo_5_pdf_generation(page, output_dir):
    """示範 5：PDF 生成（需要無頭模式）"""
    print("\n" + "=" * 60)
    print("示範 5：PDF 生成")
    print("=" * 60)
    
    # 注意：PDF 生成只能在無頭模式下使用
    print("ℹ️  注意：PDF 生成功能只能在 headless=True 模式下使用")
    print("ℹ️  以下展示 PDF 生成的程式碼範例：")
    
    code_example = '''
    # PDF 生成範例程式碼
    page.pdf(
        path="output/page.pdf",
        format="A4",
        print_background=True,
        margin={
            "top": "1cm",
            "right": "1cm",
            "bottom": "1cm",
            "left": "1cm"
        }
    )
    '''
    print(code_example)


def demo_6_video_recording():
    """示範 6：錄製影片"""
    print("\n" + "=" * 60)
    print("示範 6：錄製影片")
    print("=" * 60)
    
    current_dir = Path(__file__).parent
    output_dir = current_dir / "output"
    output_dir.mkdir(exist_ok=True)
    video_dir = output_dir / "videos"
    video_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        # 建立帶有錄影設定的 context
        context = browser.new_context(
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        
        # 載入頁面
        html_path = get_html_path()
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        print("✓ 開始錄影...")
        
        # 執行一些操作
        page.wait_for_timeout(1000)
        
        # 滾動頁面
        page.evaluate("window.scrollTo(0, 300)")
        page.wait_for_timeout(500)
        
        # 點擊按鈕
        page.click("#actionBtn1")
        page.wait_for_timeout(500)
        
        page.click("#actionBtn2")
        page.wait_for_timeout(500)
        
        # 滾動到底部
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        
        # 滾動回頂部
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)
        
        # 取得影片路徑
        video_path = page.video.path()
        
        # 關閉以完成錄影
        page.close()
        context.close()
        browser.close()
        
        print(f"✓ 錄影完成！影片儲存於：{video_path}")
        
        return video_path


def main():
    """主程式"""
    print("\n" + "📸 " + "=" * 58)
    print("📸  Playwright 截圖與錄影 - 完整示範")
    print("📸 " + "=" * 58)
    
    # 建立輸出目錄
    output_dir = create_output_dir()
    print(f"\n📁 輸出目錄：{output_dir}")
    
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(
            headless=False,
            slow_mo=300
        )
        
        # 設定視窗大小
        context = browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        
        # 載入示範頁面
        html_path = get_html_path()
        print(f"\n📄 載入頁面：{html_path}")
        
        page.goto(html_path)
        page.wait_for_load_state("networkidle")
        print("✓ 頁面載入完成")
        
        try:
            # 執行截圖示範
            demo_1_basic_screenshot(page, output_dir)
            page.wait_for_timeout(500)
            
            demo_2_element_screenshot(page, output_dir)
            page.wait_for_timeout(500)
            
            demo_3_custom_screenshot(page, output_dir)
            page.wait_for_timeout(500)
            
            demo_4_screenshot_with_actions(page, output_dir)
            page.wait_for_timeout(500)
            
            demo_5_pdf_generation(page, output_dir)
            
        except Exception as e:
            print(f"\n❌ 發生錯誤：{e}")
        
        # 關閉這個瀏覽器
        context.close()
        browser.close()
    
    # 示範錄影功能
    print("\n" + "-" * 60)
    print("準備示範錄影功能...")
    print("-" * 60)
    
    try:
        demo_6_video_recording()
    except Exception as e:
        print(f"\n❌ 錄影時發生錯誤：{e}")
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 所有示範完成！")
    print(f"📁 截圖檔案儲存於：{output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
