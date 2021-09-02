import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
URL = 'https://prolifewhistleblower.com/anonymous-form/'


def scrape(link):
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)


scrape(URL)