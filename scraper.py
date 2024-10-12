from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_stealth import stealth

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

    def quit(self):
        self.driver.quit()


# Instantiate the scraper and keep it open for 10 seconds
import time
if __name__ == "__main__":
    scraper_instance = Scraper()
    scraper_instance.search_property("Wollert","vic", 3750)
    time.sleep(10)  # Keep the browser open for 10 seconds
    scraper_instance.quit()

