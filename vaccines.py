import requests
from bs4 import BeautifulSoup
import time
import webbrowser


"""
This is a web scraper for checking when COVID vaccines are available in the cities of Houston and San Antonio.

This scraper works by taking the HTML from the page, then checking for updates. When there is a change, it opens the
webpage so that you can register for vaccines.

The scraper checks the website every 30 seconds and not quicker to avoid unnecessary traffic
"""

HOUSTON_LINK = "https://vacstrac.hctx.net/landing"
SA_LINK = "https://covid19.sanantonio.gov/Services/Vaccination-for-COVID-19"

CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

COOL_DOWN = 30


def check_url(link):
    page = requests.get(link)
    original = BeautifulSoup(page.content, "html.parser")
    run = True
    while run:
        reloaded = requests.get(link)
        nuevo = BeautifulSoup(reloaded.content, "html.parser")
        if original != nuevo:
            run = False
            webbrowser.get(CHROME_PATH).open(link)
        time.sleep(COOL_DOWN)


check_url(SA_LINK)