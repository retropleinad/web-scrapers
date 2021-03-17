import requests
from bs4 import BeautifulSoup

HOUSE_LINK = "https://house.texas.gov/members/member-page/?district={0}"

HOUSE_FILE = "house.txt"


def scrape(link):
    for i in range(1, 151):
        entries = scrape_one(link, i)
        output("house.txt", entries)


def scrape_one(link, district):
    area_code = "512"
    link = link.format(str(district))
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find("div", {"class": "member-info"})

    email = soup.find("h4", {"class": "button-email"}).find(href=True)
    out = {
        "name": soup.find("h2").get_text(),
        "district": "District {0}".format(str(district)),
        "email": format_href(email),
        "phone": soup.find(string=lambda text: area_code in text).replace("\n", "", 2) \
                                                                 .replace("\r", "") \
                                                                 .strip(),
        "room": soup.find(string=lambda text: "Room" in text)
    }
    return out


def format_href(href):
    house_link = "house.texas.gov/members"
    formatted_href = str(href).split(">")[0] \
                              .split("<")[1] \
                              .split("\"")[1] \
                              .replace(".", "", 2) \
                              .replace("\n", "")
    return house_link + formatted_href


def output(file, data, delimiter=";"):
    with open(file, "a") as out:
        for key, value in data.items():
            out.write(value)
            if key != "room":
                out.write(delimiter)
        out.write("\n")


def main():
    scrape(HOUSE_LINK)


if __name__ == "__main__":
    main()