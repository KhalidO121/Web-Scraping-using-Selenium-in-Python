# Amazon Web Scraper
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

chrome_options = Options()

# Configuring ChromeWebDriver
chrome_options.add_argument("--disable-dev-shm")
driver = webdriver.Chrome(service=Service(),options=chrome_options)

#Function that getting the names and Brands of the Products and puts them in a dictionary.
############################################################
def get_products(product:str) :
    """Function that retrieves the names and Brands of the Products and puts them in a dictionary.

    Args:
        product (str): Product that you are searching for

    Returns:
        dict: Dictionary where key is the name of the product and value is the brand of the product
    """
    product_names = []
    product_brands = []
    product_description = {}

    driver.get("https://www.amazon.co.uk/")
    # Finding search box and sending input
    time.sleep(5)
    input = driver.find_element(by = By.ID, value="twotabsearchtextbox")
    input.send_keys(product)
    input.send_keys(Keys.ENTER)

    # Switching windows for the driver
    current_window = driver.current_window_handle
    driver.switch_to.window(current_window)

    # Getting the first pages from the search
    disabled_page_number_element = driver.find_element(By.XPATH, "//span[@class='s-pagination-item s-pagination-disabled']")
    number_of_pages = int(disabled_page_number_element.text)

    # Grabbing the names of Basketball shoes and their brands from first few pages and putting it in their respective lists
    for i in range(number_of_pages):
        print("Scraping page " + str(i+1))
        time.sleep(10)
        names_of_products = driver.find_elements(By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")
        brands_of_products = driver.find_elements(By.XPATH, "//span[@class='a-size-base-plus a-color-base']")
        for name in names_of_products:
            product_names.append(name.text)
        for brand in brands_of_products:
            product_brands.append(brand.text)
        if i == number_of_pages - 1:
            break
        else:
            next_page_button = driver.find_element(By.XPATH,"//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
            next_page_button.click()
            current_window = driver.current_window_handle
            driver.switch_to.window(current_window)
        # Putting the names and brands of the products into a dictionary
        for i in range(len(product_names)):
            product_description[product_names[i]] = product_brands[i]
            
    return product_description


if __name__ == "__main__":
    print(get_products("Basketball Shoes"))