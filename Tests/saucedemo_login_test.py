from playwright.sync_api import sync_playwright 
import pytest

# End to end Source Demo test: login > cart loop (CSS) > fill > logout

def test_saucedemo_logic():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")

    # Login
        page.fill('#user-name', "standard_user")
        page.fill('#password', "secret_sauce")
        page.click('#login-button')

    # Waiting for inventory to be visible instead of fixed timeout
        page.wait_for_selector('[data-test="inventory-container"]', timeout=10000)
        print("Logged in? Title:", page.title())

        products = [
        "add-to-cart-sauce-labs-backpack",
        "add-to-cart-sauce-labs-bike-light",
        "add-to-cart-sauce-labs-bolt-t-shirt",
        "add-to-cart-sauce-labs-onesie"
        ]

        for item in products:
         page.locator(f'[data-test="{item}"]').click()
         page.wait_for_timeout(800) 

    # Go to cart
        page.click('.shopping_cart_link')
        page.wait_for_selector('.cart_item', timeout=10000)  # at least one item

        cart_badge = page.locator('.shopping_cart_badge')
        print("Items in cart:", cart_badge.inner_text() if cart_badge.is_visible() else "0")
    
    # Checkout
        page.click('#checkout')
        page.wait_for_selector('#first-name', timeout=10000)

    # Fill info
        page.fill('#first-name', "Daniel")
        page.fill('#last-name', "Yankey")
        page.fill('#postal-code', "SW1A 1AA")  
        page.click('#continue')

        page.wait_for_selector('#finish', timeout=10000)
        page.click('#finish')

    # Success message
        page.wait_for_selector('.complete-header', timeout=10000)
        print("After checkout - message:", page.inner_text('.complete-header'))

    # Logout
        page.click('#react-burger-menu-btn')
        page.wait_for_timeout(400)
        page.click('#logout_sidebar_link')

        page.wait_for_url("https://www.saucedemo.com/", timeout=10000)
        print("After logout:", page.title())

        assert page.url.endswith("/"), "Logout failed - not back at login page"

        browser.close()