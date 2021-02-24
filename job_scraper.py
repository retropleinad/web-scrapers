import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

PROGRESSIVE_DATA_JOBS = "https://www.progressivedatajobs.org/job-postings/"


def scraper(site):
    urls = []
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")
    jobs = soup.find_all(class_="grid-heading")
    for job in jobs:
        urls.append(extract_url(str(job)))
    for url in urls:
        export(position_summary(url))


def extract_url(html):
    url = ""
    start = html.find("href")
    if start != -1:
        for i in range(start + 6, len(html)):
            if html[i] == "\"":
                break
            url += html[i]
    return url


def position_summary(site):
    page = requests.get(site)
    soup = BeautifulSoup(page.content, "html.parser")
    head = soup.find(class_="uabb-subheading uabb-text-editor").text
    subheads = head.replace("\n", "").split("|")
    description = {
        "Title": soup.find("title").text.split("|")[0].strip(),
        "Organization": subheads[0].strip(),
        "Location": subheads[1].strip(),
        "Length": subheads[2].strip(),
        "Summary": summary_finder(soup).strip(),
        "Salary": salary_finder(soup).strip(),
        "How to apply": extract_url(str(soup.find(class_="apply-button"))).strip(),
        "Date Posted": date_finder(soup).strip()
    }
    return description


def salary_finder(soup):
    html = soup.find("h3", string=lambda text: 'Salary' in text)
    i = 0
    while str(html)[0] != '$' and i < 10 and html is not None:
        html = html.next
    if i == 10:
        return "null"
    return str(html)


def date_finder(soup):
    html = soup.find("h3", string=lambda text: 'Date Posted' in text)
    for i in range(0, 4):
        html = html.next
    return str(html)


def summary_finder(soup):
    summary = ""
    html = soup.find("h2", string=lambda text: 'Position Summary' in text)
    run = True
    while run:
        html_string = str(html)
        if len(html_string) > 3 and html_string[1] == 'h' and html_string[2] == '3':
            run = False
        elif html_string[0] != '<':
            summary += html_string
        html = html.next
    return summary


# Entries: Title, organization, date
def on_list(data):
    ids = open("on_list.txt", "r")
    line = ids.readline()
    entries = line.split(",")
    while line != "":
        if entries[0] == data["Title"] and entries[1] == data["Organization"] \
                and entries[2] == data["Date Posted"] + "\n":
            return True
        line = ids.readline()
        entries = line.split(",")
    return False


def export(data):
    if on_list(data):
        return False
    ids = open("on_list.txt", "a")
    ids.write(data["Title"] + "," + data["Organization"] + "," + data["Date Posted"] + "\n")
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Jobs").sheet1
    sheet.insert_row(index=2, values=None)
    i = 1
    for x, y in data.items():
        time.sleep(5)
        sheet.update_cell(2, i, data[x])
        i += 1
    return True


def main():
    scraper(PROGRESSIVE_DATA_JOBS)


if __name__ == "__main__":
    main()
