#This is from Login_ui_test - as explained this is the Page Object Model to ensure code is clean and readabl
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.timeout = 15000 #Constant - telling Playwright slow down, take 30 seconds to locate or wait for a selector
        

    def goto(self):
        self.page.goto("https://www.saucedemo.com/") #Base URL

    def login(self, username, password):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        self.page.wait_for_selector(".inventory_list", timeout=self.timeout)
        #Locator finds inventory_list, to_be_visible checks to if it's there, expect waits 15 seconds and tells me why it failed
        expect(self.page.locator(".inventory_list")).to_be_visible(timeout=self.timeout)

    def logout(self):
        self.page.click("#react-burger-menu-btn")  #Open sidebar
        self.page.wait_for_selector("#logout_sidebar_link", state="visible", timeout=60000)  # 60s—give it room
        self.page.click("#logout_sidebar_link")
        self.page.wait_for_selector("#user-name", state="visible", timeout=self.timeout)
        expect(self.page.locator("#user-name")).to_be_visible(timeout=self.timeout)
    #After checkout, telling Playwright to open sidebar and logout. And to verify that Username is visible on the homepage
    
    def login_invalid(self, username, password):
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
        self.page.wait_for_selector(".error-message-container", state="visible", timeout=60000)
        error = self.page.locator(".error-message-container")
        expect(error).to_be_visible(timeout=self.timeout)
        expect(error).to_have_text("Epic sadface: Username and password do not match any user in this service", timeout=self.timeout)
    #After logout - verify invalid login error: "Epic sadface" banner shows
       