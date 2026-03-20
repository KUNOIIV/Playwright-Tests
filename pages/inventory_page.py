#This is from Login_ui_test - as explained this is the Page Object Model to ensure code is clean and readable

from playwright.sync_api import Page, expect


class InventoryPage: 
    def __init__(self, page: Page): 
        self.page = page 
        self.timeout = 30000 #Constant - telling Playwright slow down, take 30 seconds to locate or wait for a selector
#Created a class InventoryPage to ensure to define methods to automate it's tasks

    def sort_by_price_low_to_high(self): #Method created 
        self.page.wait_for_selector("select.product_sort_container", state="visible", timeout=self.timeout)
         #This is to tell Playwright - look for select.product_sort_container in the element and make sure it is visible and take 30 seconds to look for it
        self.page.locator("select.product_sort_container").select_option("lohi")
         #Telling Playwright to look for "select.product_sort_container" and select from low to high (lohi is python's value) 
        first_item = self.page.locator(".inventory_item_name").first
         #This tells Playwright to search for the first item by item name and then make sure it's Sauce Labs Onesie
        expect(first_item).to_have_text("Sauce Labs Onesie", timeout=self.timeout)
        expect(self.page.locator(".inventory_item_price").first).to_have_text("$7.99", timeout=self.timeout)
         #Telling Playwright to locate the inventory item "Sauce Labs Onesie" and make sure its $7.99
    
    def sort_by_z_to_a(self): #Method created
        self.page.locator("select.product_sort_container").select_option("za")
         #This is to tell Playwright - look for select.product_sort_container in the element and make sure it is visible and select from Z-A
        
        first_item = self.page.locator(".inventory_item_name").first 
        expect(first_item).to_contain_text("Test.allTheThings() T-Shirt (Red)", timeout=self.timeout)
        expect(self.page.locator(".inventory_item_name").first).to_have_text("Test.allTheThings() T-Shirt (Red)", timeout=self.timeout)
         #Telling Playwright to locate "".inventory_item_name" first then make sure the text is "Test.allTheThings() T-Shirt (Red)"

    def add_multi_to_cart(self): #Method Created
        items = [ #items as the variable
            "[data-test='add-to-cart-sauce-labs-backpack']",
            "[data-test='add-to-cart-sauce-labs-bike-light']",  #Pulled Slug ID from the element 
            "[data-test='add-to-cart-sauce-labs-bolt-t-shirt']",
            "[data-test='add-to-cart-sauce-labs-onesie']"
        ]

        #For loop to ensure it clicks all of the Slug ID
        for item in items: 
            self.page.wait_for_selector(item, state="visible", timeout=self.timeout)
            locator = self.page.locator(item) #Telling Playwright to locate item 
            locator.click(timeout=8000)
            self.page.wait_for_timeout(500) 
            #Added wait_for_selector to make sure item is there and visible 

        #Final check after both clicks
        badge = self.page.locator(".shopping_cart_badge")
        expect(badge).to_be_visible(timeout=10000)
    
    def remove_item_in_cart(self):
        item = f"[data-test='remove-sauce-labs-backpack']"
        self.page.wait_for_selector(item, state="visible", timeout=self.timeout)
        self.page.click(item, timeout=self.timeout)
        expect(self.page.locator(".shopping_cart_badge")).to_be_visible(timeout=self.timeout)
    #Method created to remove item from cart and make sure the item is visible and is removed by locating the shopping cart badge

    def go_to_cart(self):
        self.page.click(".shopping_cart_link")
        self.page.wait_for_selector(".cart_list", timeout=self.timeout)
    #Method created to go cart, telling Playwright make sure ."cart_list" is there
    def continue_shopping(self):
        self.page.click("#continue-shopping")
        self.page.wait_for_selector(".title", timeout=self.timeout)
        expect(self.page.locator(".title")).to_contain_text("Products", timeout=self.timeout)
    #Method created when you go to cart instead of processing to checkout, click continue shopping instead
    #Also to locate the ".title" and make sure it should show "Products" in the inventory page
    
    def checkout(self):
        self.page.click("#checkout")
        self.page.fill('#first-name', "Daniel")
        self.page.fill('#last-name', "Yankey")
        self.page.fill('#postal-code', "SW1A 1AA")
        self.page.click('#continue')
        self.page.wait_for_selector('#finish', timeout=self.timeout)
        self.page.click('#finish')
    #Method created to click checkout and fill user details and continue. 
    #Telling Playwright - make sure it finds "#finish" in the element and click it

    def logout(self):
        self.page.click("#react-burger-menu-btn")
        self.page.click("#logout_sidebar_link")
        expect(self.page.locator("#user-name")).to_be_visible(timeout=self.timeout)
    #Method created to logout and telling Playwright to locate "user-name" at the homepage after logging out