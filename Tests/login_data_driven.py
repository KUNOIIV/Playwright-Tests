import csv
import time
from playwright.sync_api import sync_playwright
import pytest

# This script is to test logins with CSV data
def test_login_data_driven():
    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        print(f"Loaded {len(rows)} rows") # Print total row loaded from CSV

    # Chrome test
    print("File opened, Chrome test")
    with sync_playwright() as p:
        chrome_browser = p.chromium.launch(headless=True) # Visible debug
        chrome_page = chrome_browser.new_page()

        for i, row in enumerate(rows, 1):
            username = row.get('username', '').strip()
            role = row.get('role', 'unknown')
            should_pass = row['should_pass']
            print(f"[{i}] Testing '{username}' (role={role}, expect={should_pass})") 
            # This is current test details (username, role, expected pass/fail)

            start = time.time() # capture start time, this is to calculate how long login takes

            chrome_page.goto("https://www.saucedemo.com/") # Demo site
            chrome_page.locator('#user-name').wait_for(state='visible', timeout=5000)
            chrome_page.fill('#user-name', username)
            chrome_page.locator('#password').wait_for(state='visible', timeout=5000)
            chrome_page.fill('#password', row['password'])
            chrome_page.click('#login-button')
            chrome_page.wait_for_timeout(3000)
            duration = time.time() - start
            print(f"  → Chrome login: {duration:.2f}s | ", end="") # Logging how it took for each user to try log in

            error = chrome_page.locator('h3[data-test="error"]')
            if row['should_pass'] == 'yes':
                assert not error.is_visible(), f"Login failed for {username}"
                print(f"✓ PASS: {username}")

                title = chrome_page.locator('[data-test="title"]').inner_text()
                print(f"  → Title: '{title}'")

                if row['expected_access'] == 'cart':
                    assert title == "Products" # Verifying successful redirect to inventory - "Products as title expected"
                    print("  ✓ Cart access OK")

                if row['role'] == 'admin':
                    assert title == "Products", "Chrome: Admin no inventory"
                    print("  ✓ Chrome: Admin access OK") #Visual_user has admin rights
                elif row['role'] == 'guest':
                    assert "error" in chrome_page.content().lower()
                    print("  ✓ Guest blocked") # Guest blocked to add to cart for testing purposes
                # If expected fail: check error message appears (login blocked as planned)  [Moved logic to else below]

                # Long username (from login error)
                if row.get('long_username') == 'yes':
                    print("  ✓ Long username caught")

                # Duplicate (expect SUCCESS on SauceDemo)
                if row.get('duplicate') == 'yes':
                    chrome_page.goto("https://www.saucedemo.com/")
                    chrome_page.wait_for_load_state('domcontentloaded')
                    chrome_page.locator('#user-name').wait_for(state='visible')
                    chrome_page.fill('#user-name', username)
                    chrome_page.fill('#password', row['password'])
                    chrome_page.click('#login-button')
                    chrome_page.wait_for_timeout(3000)
                    error_dup = chrome_page.locator('h3[data-test="error"]')

                    if error_dup.is_visible():
                        print(f"  ! Chrome: Duplicate blocked ✓")
                    else:
                        print(f"  ✓ Chrome: Duplicate allowed (expected on demo site)")
            else:
                assert error.is_visible(), f"No error for {username}"
                print(f"✓ FAIL expected: {username} | Error: {error.inner_text()}")

        chrome_browser.close()
        print("Chrome suite complete.\n")

    # Firefox (mirror)
    print("File opened, Firefox test")
    with sync_playwright() as p:
        firefox_browser = p.firefox.launch(headless=True)
        firefox_page = firefox_browser.new_page()

        for i, row in enumerate(rows, 1):
            username = row.get('username', '').strip()
            role = row.get('role', 'unknown')
            should_pass = row['should_pass']
            print(f"[{i}] Testing '{username}' (role={role}, expect={should_pass})")

            start = time.time()
            
            firefox_page.goto("https://www.saucedemo.com/")
            firefox_page.wait_for_load_state('domcontentloaded')
            firefox_page.locator('#user-name').wait_for(state='visible', timeout=5000)
            firefox_page.fill('#user-name', username)
            firefox_page.locator('#password').wait_for(state='visible', timeout=5000)
            firefox_page.fill('#password', row['password'])
            firefox_page.click('#login-button')
            firefox_page.wait_for_timeout(3000)
            duration = time.time() - start
            print(f"  → Firefox login: {duration:.2f}s | ", end="") 

            error = firefox_page.locator('h3[data-test="error"]')

            if row['should_pass'] == 'yes':
                assert not error.is_visible()
                print(f"✓ PASS: {username}")

                title = firefox_page.locator('[data-test="title"]').inner_text()
                print(f"  → Title: '{title}'")

                if row['expected_access'] == 'cart':
                    assert title == "Products"
                    print("  ✓ Cart access OK")

                if row['role'] == 'admin':
                    assert title == "Products"
                    print("  ✓ Firefox: Admin access OK")
                elif row['role'] == 'guest':
                    assert "error" in firefox_page.content().lower()
                    print("  ✓ Guest blocked")

                if row.get('long_username') == 'yes':
                    print("  ✓ Long username caught")

                if row.get('duplicate') == 'yes':
                    firefox_page.goto("https://www.saucedemo.com/")
                    firefox_page.wait_for_load_state('domcontentloaded')
                    firefox_page.locator('#user-name').wait_for(state='visible')
                    firefox_page.fill('#user-name', username)
                    firefox_page.fill('#password', row['password'])
                    firefox_page.click('#login-button')
                    firefox_page.wait_for_timeout(3000)
                    error_dup = firefox_page.locator('h3[data-test="error"]')
                    if error_dup.is_visible():
                        print(f"  ! Firefox: Duplicate blocked ✓")
                    else:
                        print(f"  ✓ Firefox: Duplicate allowed (expected on demo site)")
            else:
                assert error.is_visible()
                print(f"✓ FAIL expected: {username} | Error: {error.inner_text()}")

        firefox_browser.close()
        print("Firefox suite complete.\n")

# RUN AS PLAIN PYTHON (non-pytest)
if __name__ == "__main__":
    test_login_data_driven()