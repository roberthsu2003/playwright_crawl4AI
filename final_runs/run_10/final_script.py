"""台灣銀行牌告匯率查詢 CLI 工具。

從台灣銀行牌告匯率頁面擷取指定幣別的現金買入與現金賣出匯率。

使用範例：
    python final_script.py                  # 查詢 USD（預設）
    python final_script.py --currency EUR   # 查詢歐元
    python final_script.py --currency JPY   # 查詢日幣
"""

import asyncio
import datetime
import os
import sys
from typing import Optional

_URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"


def _resolve_run_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def _make_logger(log_path: str):
    def log(msg: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return log


async def _run(currency: str) -> dict:
    from playwright.async_api import async_playwright

    run_dir = _resolve_run_dir()
    screenshot_dir = os.path.join(run_dir, "screenshots")
    log_path = os.path.join(run_dir, "final_script_log.txt")
    os.makedirs(screenshot_dir, exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")

    log = _make_logger(log_path)

    currency = currency.upper().strip()
    log(f"step 0 params: currency={currency}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 1800})

        # CP1: 導航
        log("step 1 action: 導航至台灣銀行牌告匯率頁面")
        await page.goto(_URL, wait_until="networkidle")
        await page.screenshot(
            path=os.path.join(screenshot_dir, "final_execution_1_navigate.png")
        )
        log(f"  頁面標題: {await page.title()}")

        # CP2: 確認表格載入
        log("step 2 action: 確認匯率表格已載入")
        await page.wait_for_selector("table tbody tr", timeout=10000)
        rows = await page.query_selector_all("table tbody tr")
        log(f"  表格列數: {len(rows)}")
        await page.screenshot(
            path=os.path.join(screenshot_dir, "final_execution_2_table.png")
        )

        # CP3: 定位幣別列
        log(f"step 3 action: 定位 {currency} 列")
        target_row = None
        for row in rows:
            text = await row.inner_text()
            if f"({currency})" in text or f" {currency}" in text:
                target_row = row
                break

        if target_row is None:
            log(f"  錯誤：找不到幣別代碼 {currency}，請確認代碼正確")
            await browser.close()
            return {"error": f"幣別 {currency} 不存在", "currency": currency}

        row_text = await target_row.inner_text()
        currency_name = row_text.split("\n")[0].strip()
        log(f"  找到列: {currency_name}")

        # CP4 & CP5: 擷取匯率
        log("step 4 action: 擷取現金買入與現金賣出匯率")
        tds = await target_row.query_selector_all("td")
        cash_buy  = (await tds[1].inner_text()).strip()
        cash_sell = (await tds[2].inner_text()).strip()
        log(f"  現金買入: {cash_buy}")
        log(f"  現金賣出: {cash_sell}")

        await target_row.scroll_into_view_if_needed()
        await page.screenshot(
            path=os.path.join(screenshot_dir, "final_execution_3_target_row.png")
        )

        # CP6: 輸出結果
        log("step 5 action: 輸出最終結果")
        log("=" * 45)
        log(f"  台灣銀行 {currency_name} 牌告匯率")
        log(f"  現金買入（銀行向您收購）: {cash_buy} TWD")
        log(f"  現金賣出（銀行賣給您）:   {cash_sell} TWD")
        log("=" * 45)

        await browser.close()

    return {
        "currency": currency,
        "currency_name": currency_name,
        "cash_buy": cash_buy,
        "cash_sell": cash_sell,
    }


def lookup_exchange_rate(currency: str = "USD") -> dict:
    """從台灣銀行牌告匯率頁面查詢指定幣別兌台幣的現金匯率。

    Args:
        currency: 幣別的 ISO 4217 代碼（不區分大小寫）；例如 "USD"、"EUR"、
            "JPY"、"GBP"、"AUD"、"CAD"。需為台灣銀行支援的幣別。
            Default: "USD".

    Returns:
        dict，包含以下鍵：
            ``currency`` (str): 輸入的幣別代碼（轉大寫後）。
            ``currency_name`` (str): 台灣銀行顯示的幣別全名（含代碼）。
            ``cash_buy`` (str): 現金買入匯率（銀行向客戶收購外幣的價格）。
            ``cash_sell`` (str): 現金賣出匯率（銀行賣給客戶外幣的價格）。
            ``error`` (str, optional): 若幣別不存在則回傳錯誤訊息。
    """
    return asyncio.run(_run(currency=currency))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=lookup_exchange_rate.__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "範例:\n"
            "  python final_script.py                  # 查詢 USD（預設）\n"
            "  python final_script.py --currency EUR   # 查詢歐元\n"
            "  python final_script.py --currency JPY   # 查詢日幣\n"
        ),
    )
    parser.add_argument(
        "--currency",
        dest="currency",
        type=str,
        default="USD",
        metavar="CODE",
        help=(
            "幣別的 ISO 4217 代碼（不區分大小寫）；"
            "例如 USD、EUR、JPY、GBP。預設: USD"
        ),
    )
    args = parser.parse_args()
    result = asyncio.run(_run(**vars(args)))
    print(result)
