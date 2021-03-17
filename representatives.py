import requests
from bs4 import BeautifulSoup

HOUSE_LINK = "https://house.texas.gov/members/member-page/?district={0}"
SENATE_LINK = "https://senate.texas.gov/members.php?d={0}"

HOUSE_MEMBERS = 150
SENATE_MEMBERS = 30


def scrape_all(link, members):
    for i in range(1, members + 1):
        scrape(link, i)


def scrape(link, number):
    area_code = "(512)"
    link = link.format(str(number))
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find("div", {"class": "member-info"})

    out = {
        "name": soup.find("h2").get_text(),
        "district": "District {0}".format(str(number)),
        "email": format_href(soup.find("h4", {"class": "button-email"}).find(href=True)),
        "phone": soup.find(string=lambda text: area_code in text),
        "room": soup.find(string=lambda text: "Room" in text)
    }

    for key, value in out.items():
        print(value)
    return out


def format_href(href):
    house_link = "house.texas.gov/members"


def output(file):
    pass


scrape_all(HOUSE_LINK, HOUSE_MEMBERS)