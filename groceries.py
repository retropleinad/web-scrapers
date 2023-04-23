import requests
import urllib.request
import time
import webbrowser

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer': 'https://www.google.com/'
}

BASE_URL = 'https://shop.wegmans.com/search?search_term={term}'


# Search with bs4 and requests with special header
# Still returns JavaScript error
def header_search_item(item):
    search_url = BASE_URL.format(term=item)
    page = requests.get(search_url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)


def urllib_search_item(item):
    search_url = BASE_URL.format(term=item)
    page = urllib.request.urlopen(search_url)
    soup = BeautifulSoup(page, 'html.parser')
    print(soup)


def selenium_search_item(item):
    search_url = BASE_URL.format(term=item)
    driver = webdriver.Chrome()
    driver.get(search_url)

    # print(driver.page_source)
    # store = driver.find_element(By.XPATH, '//*[contains(text(), \'Fairfax\')]')
    # print(store)

    # new_html = driver.page_source.replace('Fairfax', 'Bethlehem')

    # driver.execute_script(new_html)
    # webbrowser.open(new_html)

    first_item = driver.find_element(By.CLASS_NAME, 'css-8uhtka')
    print(first_item.get_attribute('innerHTML'))

    driver.quit()


def js_from_file():
    driver = webdriver.Chrome()
    with open('wegmans_augmented.js', mode='r') as js_file:
        js_text = js_file.read()
        driver.execute_script(js_text)
        print(driver.page_source)


def html_from_file():
    driver = webdriver.Chrome()
    driver.get('file://choose_store.html')
    print(driver.page_source)


def search_steps(item):
    driver = webdriver.Chrome()
    initial_url = 'https://www.wegmans.com/stores/bethlehem-pa/'
    driver.get(initial_url)
    print(driver.title)

    shop_store_button = driver.find_element(By.XPATH, '//*[contains(text(), \'Shop this Store\')]')
    driver.execute_script('arguments[0].click();', shop_store_button)
    # button.click()
    print(driver.title)
    time.sleep(60)
    print(driver.title)

    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for b in buttons:
        if b.text == 'In Store':
            print(b.get_attribute('innerHTML'))
            b.click()
            time.sleep(30)
            break

    search_bars = driver.find_elements(By.TAG_NAME, 'input')
    # in_store_button = driver.find_elements(By.XPATH, '//*[contains(text(), \'In Store\')]')
    # search_bars = driver.find_elements(By.TAG_NAME, 'Form')
    # search_bars = driver.find_elements(By.XPATH, '//button[@type=\'submit\']')

    # Issue: shop this store button isn't executing correctly

    search_bar = ''
    for s in search_bars:
        try:
            s.click()
            s.send_keys('rice')
            s.submit()
            search_bar = s
            print(s.get_attribute('innerHTML'))
            break
        except Exception:
            pass
        finally:
            time.sleep(15)

    first_item = driver.find_element(By.CLASS_NAME, 'css-8uhtka')
    print(first_item.get_attribute('innerHTML'))

    """
    for item in items:
        if len(item.get_attribute('innerHTML')) < 5:
            print(item.get_attribute('innerHTML'))
    i = 3
    """


# header_search_item('rice')
# selenium_search_item('rice')
print('lolwtf')
search_steps('rice')

