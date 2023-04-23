import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException


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
        self.search_bar.send_keys(item)
        section = self.driver.find_element(By.CLASS_NAME, 'css-8uhtka')
        return section

    def quit(self):
        self.driver.quit()


scraper = WegmanScraper()
