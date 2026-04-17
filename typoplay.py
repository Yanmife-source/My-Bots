from playwright.sync_api import sync_playwright
import time

#It seems Playwright isn't necessarily faster than Selenium
text=input("Enter a product to search for: ")
with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context=browser.new_context()
    page=context.new_page()

    page.goto('https://www.konga.com')
    time.sleep(1)
    page.get_by_role("search",name="Search Box").fill(text)
    time.sleep(2.5)
    browser.close

