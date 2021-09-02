from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

URL = 'https://prolifewhistleblower.com/anonymous-form/'
PATH = 'D:\Programs\ChromeDriver\chromedriver.exe'


def tutorial():
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get('http://www.python.org')
    assert 'Python' in driver.title
    elem = driver.find_element_by_name('q')
    elem.clear()
    elem.send_keys('pycon')
    elem.send_keys(Keys.RETURN)
    assert 'No Results found.' not in driver.page_source
    driver.close()


def scrape(link):
    driver = webdriver.Chrome(executable_path=PATH)
    driver.get(link)
    element = driver.find_element_by_class_name('forminator-class')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)
    print(element)
    driver.close()


scrape(URL)