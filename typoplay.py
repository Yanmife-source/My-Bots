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
        extra_headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
        context=browser.new_context(extra_http_headers=extra_headers)
        page=context.new_page()
        try:
            url=f"https://www.konga.com/search?search={product.replace(' ', '+')}"
            response=page.goto(url,wait_until="domcontentloaded",timeout=10000)
            page.wait_for_timeout(2500) 
            print(f"{page.url} | {response.status}:{response.status_text}")
        except Exception as e:
            sys.exit(f"Error scraping: {str(e)}")
        finally:
            browser.close()

if __name__=="__main__":
    main()

