import os
import sys
from dotenv import load_dotenv
load_dotenv()
from playwright.async_api import async_playwright
import asyncio
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

async def scrape_site(async_play,url):
    """Opens a URL, waits for JavaScript to load, and dumps all visible text."""
    browser = await async_play.chromium.launch(
        headless=True,
        executable_path="/usr/bin/chromium",
        args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
    context=await browser.new_context()
    page= await context.new_page()
    try:
        # Set a standard user agent so the sites don't immediately block you
        await page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        await page.goto(url, wait_until="load", timeout=15000)
        await page.wait_for_timeout(3000) # Wait 3 seconds for prices to fully render
        
        # Grab all the visible text on the page
        page_text = await page.locator("body").inner_text()
        return page_text
    except Exception as e:
        return f"Error scraping: {str(e)}"
    finally:
        await browser.close()
    

async def main():
# Get product from command line
    try:
        product = sys.argv[1]
        if len(sys.argv)>2:
            sys.exit("Usage: python scraper_agent.py <product_name>")
        
    except IndexError:
        sys.exit(
            "No product specified.\n"
            "Usage: python scraper_agent.py <product_name>\n"
            "Example: python scraper_agent.py crocs"
        )

    # Build the search URL dynamically based on product
    urls ={ "Konga":f"https://www.konga.com/search?search={product.replace(' ', '+')}",
        "Jumia":f"https://jumia.com.ng/catalog/?q={product.replace(' ','+')}",
        "Jiji":f"https://jiji.ng/search?query={product.replace(' ','+')}"
    }

    print(f"Searching prices of : '{product}'...")
    raw_site_text=""


    # Define the llm
    groq_llm = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.1
    )

    print(f"Searching prices of : '{product}'...")

    raw_scraped_data="" 
    async with async_playwright() as ap:
        async with asyncio.TaskGroup() as tg:
            tasks={}
            for site,url in urls.items():
                print(f"📦 Fetching first page data from {site}...")
                tasks[site] = tg.create_task(scrape_site(ap,url))

        for site, comp_task in tasks.items():
            site_text = comp_task.result()  # .result() grabs the actual string return value
            raw_scraped_data += f"\n--- DATA FROM {site} ---\n{site_text}\n"
            

    prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a precise data analysis expert. Your job is to parse raw website text dumps from Jumia, Konga, and Jiji.
            1. Scan the text and extract items matching the user's query.
            2. Identify their prices in Nigerian Naira (₦).
            3. Compare the items across the platforms and output a clean summary.
            4. Explicitly state which platform has the absolute cheapest option for the product."""),
            ("user", "Analyze and compare the prices from this raw scraped text:\n\n{scraped_text}")
        ])
    
    print("🤖 Finding the best deals with Llama3...")
    chain = prompt | groq_llm
    response = await chain.ainvoke({"scraped_text": raw_scraped_data})
    
    print("\n📊 --- FINAL PRICE COMPARISON --- 📊")
    print(response.content)
    1

if __name__ == "__main__":
    asyncio.run(main())


