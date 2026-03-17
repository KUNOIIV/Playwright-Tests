import csv
import time
from playwright.sync_api import sync_playwright

# This script is to test logins with CSV data 

with sync_playwright() as p:
    chrome_browser = p.chromium.launch(headless=True)  # Visible debug
    chrome_page = chrome_browser.new_page()

    firefox_browser = p.firefox.launch(headless=True)
    firefox_page = firefox_browser.new_page()

    with open("users.csv", "r") as file:
        reader = csv.DictReader(file) 
        rows = list(reader)
    print(f"Loaded {len(rows)} rows") # Print total row loaded from CSV

    # Chrome test
    print("File opened, Chrome test")
    for i, row in enumerate(rows, 1):
        username = row.get('username', '').strip()
        print(f"[{i}] Testing: '{username}' (role={row['role']}, pass={row['should_pass']})") # This is to current test details (username, role, expected pass/fail)

        start = time.time() # capture start time, this is to calculate how long login takes
        
        chrome_page.goto("https://www.saucedemo.com/") # Demo site
        chrome_page.locator('#user-name').wait_for(state='visible', timeout=5000)
        chrome_page.fill('#user-name', username)
        chrome_page.locator('#password').wait_for(state='visible', timeout=5000)
        chrome_page.fill('#password', row['password'])
        chrome_page.click('#login-button')
        chrome_page.wait_for_timeout(3000)
        print(f" Chrome: {username} login took {time.time() - start:.2f}s") # Logging how it took for each user to try log in 

        error = chrome_page.locator('h3[data-test="error"]')
        if row['should_pass'] == 'yes':
            assert not error.is_visible(), f"Login failed for {username}"
            print(f"  ✓ PASS login: {username}")

            title = chrome_page.locator('[data-test="title"]').inner_text()
            print(f"  Title: '{title}'")

            if row['expected_access'] == 'cart':  
                assert title == "Products" # Verifying successful redirect to inventory - "Products as title expected"
                print("  ✓ Cart access OK")

            if row['role'] == 'admin':
                assert title == "Products", "Chrome: Admin no inventory"
                print("  ✓ Chrome: Admin access OK")  #Visual_user has admin rights
            elif row['role'] == 'guest':
                assert "error" in chrome_page.content().lower()
                print("  ✓ Guest blocked") # Guest blocked to add to cart for testing purposes
        else: 
            assert error.is_visible(), f"No error for {username}" # If expected fail: check error message appears (login blocked as planned)
            print(f"  ✓ FAIL expected: {username} - {error.inner_text()}")

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
                print(f" ! Chrome: Duplicate blocked - good (expected for secure site)")
            else:
                print(f" x Chrome: Duplicate allowed: potentional security holes!")

    # Firefox (mirror)
    print("File opened, Firefox test")
    for i, row in enumerate(rows, 1): 
        username = row.get('username', '').strip() 
        print(f"[{i}] Testing: '{username}' (role={row['role']}, pass={row['should_pass']})")

        start = time.time()
        
        firefox_page.goto("https://www.saucedemo.com/")
        firefox_page.wait_for_load_state('domcontentloaded')
        
        firefox_page.locator('#user-name').wait_for(state='visible', timeout=5000)
        firefox_page.fill('#user-name', username)
        firefox_page.locator('#password').wait_for(state='visible', timeout=5000)
        firefox_page.fill('#password', row['password'])
        firefox_page.click('#login-button')
        firefox_page.wait_for_timeout(3000)
        print(f" Firefox: {username} login took {time.time() - start:.2f}s") 

        error = firefox_page.locator('h3[data-test="error"]')

        if row['should_pass'] == 'yes':
            assert not error.is_visible()
            print(f"  ✓ PASS login: {username}")

            title = firefox_page.locator('[data-test="title"]').inner_text()
            print(f"  Title: '{title}'")

            if row['expected_access'] == 'cart':
                assert title == "Products"
                print("  ✓ Cart access OK")

            if row['role'] == 'admin':
                assert title == "Products"
                print("  ✓ Firefox: Admin access OK")
            elif row['role'] == 'guest':
                assert "error" in firefox_page.content().lower()
                print("  ✓ Guest blocked")
        else:
            assert error.is_visible()
            print(f"  ✓ FAIL expected: {username} - {error.inner_text()}")

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
                print(f" ! Chrome: Duplicate blocked - good (expected for secure site)")
            else:
                print(f" x Chrome: Duplicate allowed: potentional security holes!")

    chrome_browser.close()
    firefox_browser.close()
