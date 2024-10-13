from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select

from selenium_stealth import stealth
from soupsieve.css_types import Selector


class Scraper:

    def __init__(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.website_url = "https://www.raywhite.com"
        self.driver = webdriver.Chrome(options= chrome_options)

        self.driver.get(url=self.website_url)
        self.wait = WebDriverWait(self.driver, 20)

    def search_property(self, suburb_name:str, state:str, postcode:int):

        # Click on find property button.
        find_property = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="site"]/header[1]/div[2]/div[2]/div/div[2]/ul/li[3]/button')))
        find_property.click()

        # create a address to search.
        address = f"{suburb_name},{state.upper()} {postcode}"

        # enter suburb.
        suburb = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-select-2-input"]')))
        suburb.send_keys(address)

        # wait for 5 second.
        time.sleep(5)
        suburb.send_keys(Keys.ENTER)

        # search property by suburb name.
        search = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menuFilter"]/div/div[2]/div[2]/div[3]/button')))
        search.send_keys(Keys.ENTER)
        time.sleep(5)

    def apply_filter_on_search(self, property_type_selected:str = None, bedrooms_size:int= None):

        # Select property type
        if property_type_selected is not None:
            property_type = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/div[1]/div/select')))
            property_type_selector = Select(property_type)
            property_type_selector.select_by_visible_text(property_type_selected)
            time.sleep(5)

        # Select number of bedrooms.
        if bedrooms_size is not None:
            bedrooms_dropdown = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/div[2]/div/select')))
            bedrooms_selector = Select(bedrooms_dropdown)
            bedrooms_selector.select_by_visible_text(f"+{bedrooms_size} Bedrooms")

        # search property by suburb name.
        search = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/button')))
        search.send_keys(Keys.ENTER)
        time.sleep(5)



    def quit(self):
        self.driver.quit()


# Instantiate the scraper and keep it open for 10 seconds
import time
if __name__ == "__main__":
    scraper_instance = Scraper()
    scraper_instance.search_property("Wollert","vic", 3750)
    scraper_instance.apply_filter_on_search(property_type_selected="House", bedrooms_size=2)
    time.sleep(10)  # Keep the browser open for 10 seconds
    scraper_instance.quit()

