from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
import time
from bs4 import BeautifulSoup,SoupStrainer
import csv
import sys



def main():
    # User Input
    product=sys.argv[1]
    # Configure the headless option
    options=Options()
    options.add_argument("--headless=new")

    # To specify the path to chromedriver 
    service=Service(executable_path="/home/naeve/Downloads/chromedriver-linux64/chromedriver")
    driver=webdriver.Chrome(service=service,options=options)
    
    # To navigate to the website
    global base_url
    base_url="https://jumia.com.ng"
    driver.get(base_url)
    time.sleep(1.5)

    # Wait till the search bar is present
    print("Searching...")
    search=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID,"fi-q")))
    search.send_keys(product + Keys.ENTER)

    # TO wait for the page to load
    time.sleep(1.5)
    # Parses he page for products name and price
    print("Parsing...")
    
    # Scraping logic here
    soup(driver)

    # Exit the webiste and close the browser
    driver.quit()

def soup(driver):
    prices=[]
    current_page_url = driver.current_url
    tags=SoupStrainer('a')
    for page_num in range(1, 6): # To parse the first 5 pages
        driver.get(f"{current_page_url}&page={page_num}")
        page=driver.page_source
        obe=BeautifulSoup(page,'html.parser',parse_only=tags)
        info=obe.find_all('div',class_="info")
        for  data in info:
            name=data.find('h3',class_='name').text.strip()
            new_price=data.find('div',class_='prc').text.strip()
            discount=data.find('div',class_='bdg _dsct _sm')
            if discount:
                discount=discount.text.strip()
            else:
                discount=None
        
            price_dict={}
            
            if name and new_price:
                #print( f"Product name: {name} Price: {new_price}\n")
                price_dict["Product name"]= name
                price_dict["Price"]=new_price
                prices.append(price_dict)
            else:
                print("This product couldn't be displayed")
           
            price_dict["Discount"]=discount
            
               
    headers=['Product name','Price',"Discount"]

    #Save the result to a csv file
    with open('prices.csv',"w",newline='') as prc:
        writer=csv.DictWriter(prc,fieldnames=headers)
        print('Saving to prices.csv...')
        writer.writeheader()
        writer.writerows(prices)
        print(f"Saved {len(prices)} items to prices.csv")


if __name__=="__main__":
    main()