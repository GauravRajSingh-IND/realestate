from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select

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

    def apply_filter_on_search(self, property_type_selected:str = None, bedrooms_size:int= 0, bathroom_num: int = 0,
                               parking_num:int = 0):

        # Select property type
        if property_type_selected is not None:
            property_type = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/div[1]/div/select')))
            property_type_selector = Select(property_type)
            property_type_selector.select_by_visible_text(property_type_selected)
            time.sleep(5)

        # Select number of bedrooms.
        if bedrooms_size != 0:
            bedrooms_dropdown = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/div[2]/div/select')))
            bedrooms_selector = Select(bedrooms_dropdown)
            bedrooms_selector.select_by_visible_text(f"+{bedrooms_size} Bedrooms")

        # Select number of bathroom.
        if bathroom_num != 0:
            bathrooms_dropdown = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/div[3]/div/select')))
            bathroom_selector = Select(bathrooms_dropdown)
            bathroom_selector.select_by_visible_text(f"+{bathroom_num} Bathrooms")

        # Select the parking number
        if parking_num != 0:
            parking_dropdown = self.wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/div[4]/div/select')))
            parking_selector = Select(parking_dropdown)
            parking_selector.select_by_visible_text(f"+{parking_num} Parking")


        # search property by suburb name.
        search = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/section[2]/form/div/div[2]/div[2]/button')))
        search.send_keys(Keys.ENTER)
        time.sleep(5)

        # Sort the listing to recent first.
        self.sort_by()

    def sort_by(self):

        # Sort the result by most recent listing.
        sort_by_recent = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/section/section[2]/div[2]/div[2]/div[1]/div/select')))
        sort_by_selector = Select(sort_by_recent)
        sort_by_selector.select_by_visible_text("Most Recent Listing")

        # sort by property live for auction.
        for_auction = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="root"]/section/section[2]/div[2]/div[2]/div[2]/div/select')))
        for_auction_selector = Select(for_auction)
        for_auction_selector.select_by_visible_text('For Auction')

    def quit(self):
        self.driver.quit()

    def load_data(self, num_times:int = 1):

        load_more_button = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/div/button')))

        # load data.
        for i in range(num_times):
            load_more_button.send_keys(Keys.ENTER)
            time.sleep(2)

    def scrape_listing_result(self):

        property_listings = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/section/div/div[2]')))
        ui_cards = property_listings.find_elements(By.CLASS_NAME, 'ui-card')

        # property links.
        property_links = []
        # Loop over each ui card and get details.
        for card in ui_cards:

            # get href of the property.
            href = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            property_links.append(href)

# Instantiate the scraper and keep it open for 10 seconds
import time
if __name__ == "__main__":
    scraper_instance = Scraper()
    scraper_instance.search_property("Wollert","vic", 3750)
    scraper_instance.apply_filter_on_search(property_type_selected="House", parking_num=2)
    time.sleep(2)  # Keep the browser open for 10 seconds
    scraper_instance.load_data()
    time.sleep(2)  # Keep the browser open for 10 seconds
    scraper_instance.scrape_listing_result()
    scraper_instance.quit()

