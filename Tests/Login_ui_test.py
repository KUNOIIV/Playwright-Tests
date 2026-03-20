#Page Object Model - the point of this, is to make the code more cleaner and shorter 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from playwright.sync_api import sync_playwright, Page, expect


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000) #Launch Chrome browser (visible, slow-mo for debug)
        page = browser.new_page() 
        login = LoginPage(page) #Instantiate LoginPage – pulls methods from login_page.py
        login.goto()#Navigate to base URL (https://www.saucedemo.com/)
        
        
        login.login("standard_user", "secret_sauce")
        #Login with valid credentials - the right credentials goes to the inventory page
        
        page.wait_for_selector(".title", timeout=15000)  
        expect(page.locator(".title")).to_have_text("Products", timeout=10000)
        #wait_for selector and expect(page.locator) is to prove that ".title" is inventory and "Products" is the title
        #Also added timeout to make sure it spends a little time finding the locator
        
        assert page.url.endswith("/inventory.html")

        expect(page.locator(".inventory_item").first).to_be_visible(timeout=10000)
        #This page.locator is to tell playwright - make sure that the first inventory item is on the list

        inventory = InventoryPage(page)
        #Created a class InventoryPage in inventory_page.py to peform it's methods
        
        backpack_item = "[data-test='add-to-cart-sauce-labs-backpack']"
        bike_light_item = "[data-test='add-to-cart-sauce-labs-bike-light']"
        bolt_t_shirt_item = "[data-test='add-to-cart-sauce-labs-bolt-t-shirt']"
        onesie_item = "[data-test='add-to-cart-sauce-labs-onesie']"
        #Created varibles to match the slug in the element 
       
        expect(page.locator(backpack_item)).to_be_visible(timeout=15000)
        expect(page.locator(bike_light_item)).to_be_visible(timeout=15000)
        expect(page.locator(bolt_t_shirt_item)).to_be_visible(timeout=15000)
        expect(page.locator(onesie_item)).to_be_visible(timeout=15000)
        #Created page.locator to make sure it searches the slug in the varible

        inventory.sort_by_price_low_to_high()
        inventory.sort_by_z_to_a()
        inventory.add_multi_to_cart()
        inventory.remove_item_in_cart()
        inventory.go_to_cart()
        inventory.continue_shopping()
        inventory.go_to_cart()
        inventory.checkout()
        login.logout()
        login.login_invalid("wrong_user", "pass_Wrong")
        #Chain inventory actions: sort → add/remove → cart loop → checkout. Then logout → invalid login from homepage

        expect(page.locator(".error-message-container")).to_contain_text("Epic sadface", timeout=15000)
        #Verify invalid login error: "Epic sadface" banner shows

