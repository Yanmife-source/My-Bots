from playwright.sync_api import sync_playwright
import sys
import time

#Prototype for a scraping agent uang playwright but never quite got to scraping tho,this project got boring so i paused it indefinely
def main():
    try:
        product=sys.argv[1]
        if len(sys.argv)>2:
            raise IndexError
    except IndexError:
        sys.exit("Usage: python typoplay.py <product_name>,and do not exceed one item")
    with sync_playwright() as a:
        browser= a.chromium.launch(
            headless=False,
            executable_path="/usr/bin/chromium"
            )
        context=browser.new_context()
        page=context.new_page()

        page.goto(f"https://www.konga.com/search?search={product.replace(' ', '+')}",)
        time.sleep(2.5)
        browser.close

if __name__=="__main__":
    main()

