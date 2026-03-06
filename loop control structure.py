from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) # This is to see what is going on in the browser
    page = browser.new_page()
    
    page.goto("https://www.saucedemo.com/")
    
    page.fill('[data-test="username"]', "standard_user")
    page.fill('[data-test="password"]', "secret_sauce")
    page.click('[data-test="login-button"]')
    
    page.wait_for_selector('[data-test="inventory-container"]')
    
    print("Logged in? Title:", page.title())  # Should print "Swag Labs"

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
     
     #CSS test
    items_to_add = [
        "add-to-cart-sauce-labs-backpack",
        "add-to-cart-sauce-labs-bike-light",]
    
    for test_id in items_to_add:
        page.locator(f'[data-test="{test_id}"]').click()
    
    cart_badge = page.locator('[data-test="shopping-cart-badge"]')
    print("Items in cart:", cart_badge.inner_text())
    
    browser.close()