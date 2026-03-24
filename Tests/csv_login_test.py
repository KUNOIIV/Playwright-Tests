from pages.login_page import LoginPage
import csv

def test_csv_login(page):
    login = LoginPage(page)  

    with open("Tests/users.csv", "r") as file: 
        reader = csv.DictReader(file)
        rows = list(reader) 
        print(f"Loaded {len(rows)} rows (browser={page.context.browser.browser_type.name})") #Cross Broswer test 
    # This is current test details (username, role, expected pass/fail)
    
    for i, row in enumerate(rows, 1): 
        #enumerate(rows, 1): Numbers the CSV rows like a list: Row 1, Row 2... (i=number, row=data). Logs: [1] Testing 'standard_user'
        username = row.get("username", "").strip()
        password = row.get("password", "").strip()  
        role = row.get("role", "unknown").strip()
        should_pass = row["should_pass"].strip()
        #Gets "should_pass" value from CSV row (e.g. "yes" or "no").
        print(f"[{i}] Testing '{username}' (role={role}, expect={should_pass})")

        login.goto()
        login.login(username, password)
        
        if should_pass == "yes":
            login.login_success()
            print(f"✅ PASS: {username}")
        elif should_pass == "no":
            if "locked_out" in username:  
                login.login_locked_out()
                print(f"🔒 Locked out: {username}")
            elif not username:  
                login.login_username_required()
                print(f"❌ Username required: {username}")
            else:
                login.login_invalid_creds()
                print(f"❌ Invalid creds: {username}")
    
