import requests
from bs4 import BeautifulSoup

HOUSE_LINK = "https://house.texas.gov/members/member-page/?district={0}"
SENATE_LINK = "https://senate.texas.gov/members.php?d={0}"


def scrape(link, senate=False):
    if senate:
        members = 30
    else:
        members = 150
    for i in range(1, members + 1):
        temp = scrape_one(link, i)
        print(temp["email"])


def scrape_one(link, district):
    area_code = "(512)"
    link = link.format(str(district))
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find("div", {"class": "member-info"})

    email = soup.find("h4", {"class": "button-email"}).find(href=True)
    out = {
        "name": soup.find("h2").get_text(),
        "district": "District {0}".format(str(district)),
        "email": format_href(email),
        "phone": soup.find(string=lambda text: area_code in text),
        "room": soup.find(string=lambda text: "Room" in text)
    }
    return out


def format_href(href, senate=False):
    house_link = "house.texas.gov/members"
    formatted_href = str(href).split(">")[0] \
                              .split("<")[1] \
                              .split("\"")[1] \
                              .replace(".", "", 2)
    return house_link + formatted_href


def output(file):
    pass


scrape(HOUSE_LINK)
