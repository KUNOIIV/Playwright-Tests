# QA Automation Portfolio

Automated UI & API tests using Playwright, pytest, requests + GitHub Actions CI/CD.  
Data-driven (CSV), full CRUD API checks, auto-runs on every push.  

## What it does
- UI Smoke Tests: Playwright scripts (login, CSV data-driven) — green on push.  
- API Tests: GET/POST/DELETE on jsonplaceholder (fake CRUD) — asserts status codes, JSON keys.  
- CI/CD: Runs all tests in cloud (no local server needed).
- Page Object Model (POM): Clean, reusable Pages
- Full E2E regression: Login → sort → add/remove cart → checkout → logout + invalid creds.
- Reports: HTML summary included

## Setup & Run
1. Clone repo    
2. Run locally in cmd - pytests Tests/ -v  
3. Push — GitHub Actions fires auto  

## Key Lessons Learned
- Relative paths > absolute (OneDrive trap).  
- Push CSV to repo or cloud dies.  
- Edge cases matter—test bad data, empty files.  
- Git rejects? Pull first, then push.  

## Screenshots
Chrome Cross Browser test:

[https://github.com/KUNOIIV/Playwright-Tests/blob/main/Chrome%20Cross%20Browser%20CSV%20test.png](https://github.com/KUNOIIV/Playwright-Tests/blob/main/Screenshots%20and%20Videos/Chrome%20Cross%20Browser%20CSV%20test.png)

[https://github.com/KUNOIIV/Playwright-Tests/blob/main/Chrome%20Cross%20Browser%20CSV%20test%20(2)%20.png](https://github.com/KUNOIIV/Playwright-Tests/blob/main/Screenshots%20and%20Videos/Chrome%20Cross%20Browser%20CSV%20test%20(2)%20.png) (part 2)

Firefox Cross Browswer test:

[https://github.com/KUNOIIV/Playwright-Tests/blob/main/Firefox%20Cross%20Browser%20CSV%20test.png](https://github.com/KUNOIIV/Playwright-Tests/blob/main/Screenshots%20and%20Videos/Firefox%20Cross%20Browser%20CSV%20test.png)

[https://github.com/KUNOIIV/Playwright-Tests/blob/main/Firefox%20Cross%20Browser%20CSV%20test%20(2).png](https://github.com/KUNOIIV/Playwright-Tests/blob/main/Screenshots%20and%20Videos/Firefox%20Cross%20Browser%20CSV%20test%20(2).png)

CI/CD Output results (First didn't succeed then made fixes to fix it. Now everytime pushing a new file drone will pass):

https://github.com/KUNOIIV/Playwright-Tests/blob/main/CICD%20Test%20output.png

Loop control structure adding items in cart:

[https://github.com/KUNOIIV/Playwright-Tests/blob/main/Loop%20control%20structure%20add%20inventory%20to%20cart%20.png](https://github.com/KUNOIIV/Playwright-Tests/blob/main/Screenshots%20and%20Videos/Loop%20control%20structure%20add%20inventory%20to%20cart%20.png)

API test:

[https://github.com/KUNOIIV/Playwright-Tests/blob/main/API%20test%20screenshot.png](https://github.com/KUNOIIV/Playwright-Tests/blob/main/Screenshots%20and%20Videos/API%20test%20screenshot.png)

## Videos
Playwright-Loop-Control-Add-Remove-Cart-Items:

https://github.com/KUNOIIV/Playwright-Tests/blob/main/Playwright-Loop-Control-Add-Remove-Cart-Items-CSS.mp4

Built to prove: I debug, automate, ship. Not just learning, me doing.
