from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    
    #Bad loggin test with wrong creds
    page.fill('#user-name', "wrong_user")
    page.fill('#password', "pass_Wrong")
    page.click('#login-button')
    page.wait_for_timeout(1000)
    
    #Testing error message
    error_locator = page.locator ('h3[data-test="error"]')
    print("Bad creds error:", error_locator.inner_text() if error_locator.is_visible else "No error")
    assert error_locator.is_visible(), "No error on bad login"

    #Reload locked out user 
    page.reload()
    page.wait_for_timeout(1000)
    page.fill('#user-name', "locked_out_user")
    page.fill('#password', "secret_sauce")
    page.click('#login-button')
    page.wait_for_timeout(2000)
    print("Locked error:", error_locator.inner_text if error_locator.is_visible else "No error")
    assert error_locator.is_visible(), "no error on locked user!"
    assert "locked out" in error_locator.inner_text().lower(), "wrong locked message"

    #Reload page to fill blank creds
    page.reload()
    page.wait_for_timeout(1000)
    page.fill('#user-name', "")
    page.fill('#password', "")
    page.click('#login-button')
    page.wait_for_timeout(2000)
    print("blank error:", error_locator.inner_text if error_locator.is_visible else "no error")
    assert error_locator.is_visible(), "no error on blank fields"
    assert "username is required" in error_locator.inner_text().lower(), "wrong blank message"
    print("Full blank error:", error_locator.inner_text())

    browser.close()





