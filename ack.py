from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def main():
    options=Options()
    options.add_argument("--headless=new")
    service = Service(executable_path="/home/oluwayanmife/Downloads/chromedriver-linux64/chromedriver") 
    driver=webdriver.Chrome(service=service,options=options)

    try:
        navigate(driver,"https://eportal.oauife.edu.ng/login.php")
        time.sleep(15)
    finally:
        driver.quit()


def navigate(driver,site):
    driver.get(site)

    login(driver)
 
    button=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,".btn.btn-default")))
    button.click()
    
    input_bedspace=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,"ui-15")))
    input_bedspace.click()

    input_part=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"ui-40")))
    input_part.click()


def login(driver):
    input_name=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"username")))
    input_name.send_keys("<matric no>" + Keys.ENTER)

    input_password=driver.find_element(By.ID,"password")
    input_password.send_keys("<password>" + Keys.ENTER)


if __name__=="__main__":
    main()