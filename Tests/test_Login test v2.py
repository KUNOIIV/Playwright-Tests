from playwright.sync_api import sync_playwright 
import pytest

# Tests valid login with correct credentials (Playwright form submit)
def test_login_test_v2():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=500)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")
        
        page.fill('#username', "tomsmith")
        page.fill('#password', "SuperSecretPassword!")
        page.click('button ')
    
        page.wait_for_timeout(2000)
        print("After login - h2 text:", page.inner_text('h2'))
    
    # Logout
        page.click('a[href="/logout"]')  # better selector—check inspect if needed
        page.wait_for_timeout(2000)
    
    # Print ALL visible text to spot the real message
        body_text = page.inner_text('body')
        print("After logout - body text:", body_text)
    
    browser.close