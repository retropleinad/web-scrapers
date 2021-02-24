import requests
from bs4 import BeautifulSoup
import time
import webbrowser

HOUSTON_LINK = "https://vacstrac.hctx.net/landing"

SA_LINK = "https://covid19.sanantonio.gov/Services/Vaccination-for-COVID-19"
SA_PORTAL = "https://patportal.cdpehs.com/ezEMRxPHR/html/login/newPortalReg.jsp"
SA_CODE = "DOMECOVID"

CHROME_PATH = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"


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
        time.sleep(30)


check_url(SA_LINK)