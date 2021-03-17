import requests
from bs4 import BeautifulSoup

"""
This is a web scraper to take data from each Texas House member's website over : 
    a.) Name
    b.) District Number
    c.) Email
    d.) Phone Number
    e.) Office number

This data is then output to a file in CSV format
"""

HOUSE_LINK = "https://house.texas.gov/members/member-page/?district={0}"

HOUSE_FILE = "house.txt"


# Method called to scrape data.
# Link is the portal that includes a list of every house member and a link to their websites
def scrape(link):
    for i in range(1, 151):
        entries = scrape_one(link, i)
        output(HOUSE_FILE, entries)


# Method to scrape one house member's website
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


# Formats href to output the url
def format_href(href):
    house_link = "house.texas.gov/members"
    formatted_href = str(href).split(">")[0] \
                              .split("<")[1] \
                              .split("\"")[1] \
                              .replace(".", "", 2) \
                              .replace("\n", "")
    return house_link + formatted_href


# Outputs data into a CSV
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