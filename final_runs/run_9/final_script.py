"""
台灣銀行牌告匯率擷取腳本
擷取今日美元（USD）兌台幣的現金買入與現金賣出匯率
"""

import asyncio
import datetime
import os
from playwright.async_api import async_playwright

RUN_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(RUN_DIR, "screenshots")
LOG_PATH = os.path.join(RUN_DIR, "final_script_log.txt")
URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def log(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

async def main():
    # 清空 log
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 1800})

        # CP1: 導航至台灣銀行牌告匯率頁面
        log("step 1 action: 導航至台灣銀行牌告匯率頁面")
        await page.goto(URL, wait_until="networkidle")
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "final_execution_1_navigate.png")
        )
        title = await page.title()
        log(f"  頁面標題: {title}")

        # CP2: 確認匯率表格可見
        log("step 2 action: 確認匯率表格已載入")
        await page.wait_for_selector("table tbody tr", timeout=10000)
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "final_execution_2_table_loaded.png")
        )
        rows = await page.query_selector_all("table tbody tr")
        log(f"  表格列數: {len(rows)}")

        # CP3: 定位美元（USD）列
        log("step 3 action: 定位美元 (USD) 列")
        usd_row = None
        for row in rows:
            text = await row.inner_text()
            if "USD" in text:
                usd_row = row
                break

        if usd_row is None:
            log("  錯誤：找不到美元 (USD) 列")
            await browser.close()
            return

        row_text = await usd_row.inner_text()
        log(f"  找到 USD 列: {row_text.split(chr(10))[0].strip()}")

        # CP4 & CP5: 擷取現金買入與現金賣出匯率
        log("step 4 action: 擷取現金買入與現金賣出匯率")
        tds = await usd_row.query_selector_all("td")
        cash_buy  = (await tds[1].inner_text()).strip()
        cash_sell = (await tds[2].inner_text()).strip()
        log(f"  美元現金買入 (本行買入): {cash_buy}")
        log(f"  美元現金賣出 (本行賣出): {cash_sell}")

        # 截圖記錄 USD 列
        await usd_row.scroll_into_view_if_needed()
        await page.screenshot(
            path=os.path.join(SCREENSHOT_DIR, "final_execution_3_usd_row.png")
        )

        # CP6: 輸出最終結果
        log("step 5 action: 輸出最終結果")
        log("=" * 40)
        log(f"  今日台灣銀行 USD/TWD 牌告匯率")
        log(f"  現金買入（銀行向您收購）: {cash_buy} 元")
        log(f"  現金賣出（銀行賣給您）:   {cash_sell} 元")
        log("=" * 40)

        await browser.close()

asyncio.run(main())
