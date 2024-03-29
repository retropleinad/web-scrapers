"""
Web scraper that pulls the aisle an item is on from the Wegmans website.
This is part of a larger project that includes a grocery spreadsheet.
The data generated from this scraper allows sorting and filtering by aisle in the spreadsheet.
"""


import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# URL that is formatted to search for a grocery item
BASE_URL = 'https://shop.wegmans.com/search?search_term={term}'


"""
WegmanScraper:

Description: Selenium scraper wrapper that enables searching the Wegmans store for an item's aisle location

Methods:
1.) search_item(self, item): 
2.) quit(self): Quits the Selenium scraper object
"""


class WegmanScraper:

    def __init__(self):
        # initiate web driver and go to the Bethlehem store page
        # future update: allow customization for which store
        self.driver = webdriver.Chrome()
        self.initial_url = 'https://www.wegmans.com/stores/bethlehem-pa/'
        self.driver.get(self.initial_url)

        # Find button that reads 'shop store' and click it
        # This allows us to set the store we're searching to Bethlehem
        shop_store_button = self.driver.find_element(By.XPATH, '//*[contains(text(), \'Shop this Store\')]')
        self.driver.execute_script('arguments[0].click();', shop_store_button)
        time.sleep(60)

        # Find and select 'in store' button so that we can search for an item
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        for b in buttons:
            if b.text == 'In Store':
                b.click()
                time.sleep(30)
                break

        # Find search bar item that actually works and save it
        search_bars = self.driver.find_elements(By.TAG_NAME, 'input')
        self.search_bar = None
        for s in search_bars:
            try:
                s.click()
                s.send_keys('rice')
                s.submit()
                self.search_bar = s
                break
            except Exception:
                pass
            finally:
                time.sleep(15)

    # Search for item on the Wegmans site
    # Returns the aisle location of the item
    def search_item(self, item):
        # Search for the item in the search bar
        self.search_bar.click()
        self.search_bar.send_keys(Keys.CONTROL + "a")
        self.search_bar.send_keys(Keys.DELETE)
        self.search_bar.send_keys(item)
        self.search_bar.submit()
        time.sleep(30)

        # Grab the aisle location of the first instance of the item
        section = self.driver.find_element(By.CLASS_NAME, 'css-8uhtka')
        return section.text

    def quit(self):
        self.driver.quit()


"""
parse_input:

Description: Takes input file with grocery items and outputs item and aisle to an output file.
Also prints item and aisle as the script runs.

params:
1.) in_file_name: the name of the input file
2.) out_file_name: the name of the output file to be generated.
    If this file already exists, it will be deleted.
    
File format:
1.) input file: txt file where each grocery item is a new line
2.) output file: csv where each line is in the format of item, aisle
"""


def parse_input(in_file_name, out_file_name):
    searches = []
    with open(in_file_name, mode='r') as input_file:
        scraper = WegmanScraper()

        # Pulls item from file and searches in store
        ingredient = input_file.readline().strip()
        while ingredient != '':
            location = scraper.search_item(ingredient)
            print(ingredient + "," + location)
            searches.append((ingredient, location))
            ingredient = input_file.readline().strip()

        scraper.quit()

    # Check if the output file exists and remove it if it does
    if os.path.isfile(out_file_name):
        os.remove(out_file_name)

    # Output items and aisles to the output file in csv format
    # Format: item, aisle
    with open(out_file_name, newline='', mode='a') as output_file:
        for search in searches:
            output_file.write(search[0] + ", " + search[1])


parse_input('groceries_import', 'groceries_export.csv')