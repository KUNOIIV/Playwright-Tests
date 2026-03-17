from playwright.sync_api import sync_playwright
import pytest

def test_login_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://google.com")
    # Handle cookie banner
    try:
        page.click('button:has-text("Reject all")', timeout=5000)
    except:
        pass
    # Wait for search bar to be ready
    page.wait_for_selector('input[name=".gLFyf"] ', state='visible', timeout=10000)
    # Type and search
    page.fill('input[name=".gLFyf"]', "playwright test")
    page.press('input ', "Enter")
    page.wait_for_timeout(5000)  # watch it
    print("Title:", page.title())
    browser.close()