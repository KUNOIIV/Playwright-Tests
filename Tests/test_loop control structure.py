from playwright.sync_api import sync_playwright
import pytest

# Cart addition test - CSS locators to click 'Add to cart' buttons
def test_loop_control_structure():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500) # This is to see what is going on in the browser
        page = browser.new_page()
    
        page.goto("https://www.saucedemo.com/")
    
        page.fill('[data-test="username"]', "standard_user")
        page.fill('[data-test="password"]', "secret_sauce")
        page.click('[data-test="login-button"]')
    
        page.wait_for_selector('[data-test="inventory-container"]')
    
        print("Logged in? Title:", page.title())

    #CSS test, Loops through products, add each to cart, checks count
        items_to_add = [ 
         "add-to-cart-sauce-labs-backpack", 
         "add-to-cart-sauce-labs-bike-light",
         "add-to-cart-sauce-labs-bolt-t-shirt",
         "add-to-cart-sauce-labs-fleece-jacket"
        ]
    
        for test_id in items_to_add:
            page.locator(f'[data-test="{test_id}"]').click()
            print(f" Added: {test_id}")
            
            cart_badge = page.locator('[data-test="shopping-cart-badge"]')
            print("Items in cart:", cart_badge.inner_text()) 

    # Removing items in the cart then to print how many are in actually in the cart
            remove_items = [
            "remove-sauce-labs-backpack",
            "remove-sauce-labs-bike-light"
            ]
    
        for test_id in remove_items:
            page.locator(f'[data-test="{test_id}"]').click()
            print(f"Removed: {test_id}")
            print(f"Cart now:", page.locator('[data-test="shopping-cart-badge"]').inner_text())
    
            print("Final cart: 2")

        browser.close()

# RUN AS PLAIN PYTHON (non-pytest)
if __name__ == "__main__":
    test_loop_control_structure()