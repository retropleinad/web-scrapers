import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


BASE_URL = 'https://shop.wegmans.com/search?search_term={term}'


class WegmanScraper:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.initial_url = 'https://www.wegmans.com/stores/bethlehem-pa/'
        self.driver.get(self.initial_url)

        shop_store_button = self.driver.find_element(By.XPATH, '//*[contains(text(), \'Shop this Store\')]')
        self.driver.execute_script('arguments[0].click();', shop_store_button)
        time.sleep(60)

        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        for b in buttons:
            if b.text == 'In Store':
                b.click()
                time.sleep(30)
                break

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

    def search_item(self, item):
        self.search_bar.click()
        self.search_bar.send_keys(Keys.CONTROL + "a")
        self.search_bar.send_keys(Keys.DELETE)
        self.search_bar.send_keys(item)
        self.search_bar.submit()
        time.sleep(30)

        section = self.driver.find_element(By.CLASS_NAME, 'css-8uhtka')
        return section.text

    def quit(self):
        self.driver.quit()


def parse_input(in_file_name, out_file_name):
    searches = []
    with open(in_file_name, mode='r') as input_file:
        scraper = WegmanScraper()

        ingredient = input_file.readline()
        while ingredient != '':
            ingredient = input_file.readline().strip()
            location = scraper.search_item(ingredient)
            print(ingredient + "," + location)
            searches.append((ingredient, location))

        scraper.quit()

    if os.path.isfile(out_file_name):
        os.remove(out_file_name)

    with open(out_file_name, newline='', mode='a') as output_file:
        for search in searches:
            output_file.write(search[0] + ", " + search[1])


parse_input('groceries_import', 'groceries_export.csv')