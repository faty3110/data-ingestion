from selenium import webdriver
import time
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome()
web_page = 'https://www.producthunt.com/search?q=note%20taking%20ai'
driver.get(web_page)

time.sleep(5)

products = driver.find_elements(By.CLASS_NAME, "styles_item__2Fz9K")
for product in products :
    print(product.text)

driver.quit()