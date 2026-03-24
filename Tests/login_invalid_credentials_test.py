from playwright.sync_api import expect
import pytest

# Invalid login test - verifies server rejects bad credentials (status 401, shows "Invalid alert")
def test_login_invalid_credentials_test(page):  # ← Use 'page' fixture (no manual launch/close)
    page.goto("https://www.saucedemo.com/")  # ← Direct on page fixture
    
    # Scenario 1: Bad login test with wrong creds
    page.fill('#user-name', "wrong_user")
    page.fill('#password', "pass_Wrong")
    page.click('#login-button')
    page.wait_for_timeout(1000)
    
    # Testing error message
    error_locator = page.locator('h3[data-test="error"]')
    print("Bad creds error:", error_locator.inner_text() if error_locator.is_visible() else "No error")
    assert error_locator.is_visible(), "No error on bad login"
    
    # Reload for locked out user 
    page.reload()
    page.wait_for_timeout(1000)
    page.fill('#user-name', "locked_out_user")
    page.fill('#password', "secret_sauce")
    page.click('#login-button')
    page.wait_for_timeout(2000)
    print("Locked error:", error_locator.inner_text() if error_locator.is_visible() else "No error")
    assert error_locator.is_visible(), "no error on locked user!"
    assert "locked out" in error_locator.inner_text().lower(), "wrong locked message"
    
    # Reload page to fill blank creds
    page.reload()
    page.wait_for_timeout(1000)
    page.fill('#user-name', "")
    page.fill('#password', "")
    page.click('#login-button')
    page.wait_for_timeout(2000)
    print("Blank error:", error_locator.inner_text() if error_locator.is_visible() else "no error")
    assert error_locator.is_visible(), "no error on blank fields"
    assert "username is required" in error_locator.inner_text().lower(), "wrong blank message"
    print("Full blank error:", error_locator.inner_text())







