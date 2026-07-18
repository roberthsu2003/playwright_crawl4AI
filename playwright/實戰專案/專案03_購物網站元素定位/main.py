"""專案 03：用多種穩定定位方式完成 SauceDemo 購物任務。"""

import re

from playwright.sync_api import expect, sync_playwright


URL = "https://www.saucedemo.com/"


with sync_playwright() as playwright:
    playwright.selectors.set_test_id_attribute("data-test")
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)

    # label 與 placeholder 定位
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))

    # 以文字篩選特定商品卡片，再在卡片內定位按鈕
    product = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    name = product.locator(".inventory_item_name").inner_text()
    price = product.locator(".inventory_item_price").inner_text()
    product.get_by_role("button", name="Add to cart").click()

    # test id 定位
    page.get_by_test_id("shopping-cart-link").click()
    expect(page.locator(".cart_item")).to_have_count(1)

    print(f"已加入購物車: {name} / {price}")
    print("購物車數量: 1")
    browser.close()
