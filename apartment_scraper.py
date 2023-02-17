"""
apartment_scraper.py

About: This script pulls apartment listings from apartments.com that match a certain criteria.
This script then appends walkability information for each apartment from walkscore.com

Functions:
1.) build_walkscore_link: Takes an address and creates a walkscore.com link
2.) build_apartments_link: Takes city, state, and search criteria and creates an apartments.com search link
3.) get_scores: Takes a walkscore.com link and grabs the scores from the html
4.) append_walkscore: Takes a dict of apartments.com information and appends walk/transit/bike score
5.) get_apartments: Parses apartments.com HTML and outputs data to a csv
6.) main: where we run multiple searches for different cities
"""


import requests
import json
import time
import csv
import os

from bs4 import BeautifulSoup
from datetime import datetime


header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer': 'https://www.google.com/'
}


# Creates the link to search for an address on walkscore.com
def build_walkscore_link(street_address, city, state_code, zip_code=''):
    out = 'https://www.walkscore.com/score/'
    out += street_address + '-' + city + '-' + state_code

    if zip_code != '':
        out += '-' + zip_code
    return out


# Creates the link to search for apartments on apartments.com
# Takes address, apartments.com bb search filter, as well as filters for amenities
# State must be state code
def build_apartments_link(city, state, page=1, bb=None, under=2000,
                          air_conditioning=True, washer_dryer=True, dishwasher=True,
                          parking=True, pool=True, patio=True):

    # Create link to return and include city, state, and under price limit
    out = 'https://www.apartments.com/{city}-{state}/under-{under}/'.format(city=city, state=state, under=under)

    # Append conditional searches to the string
    if air_conditioning:
        out += 'air-conditioning-'
    if washer_dryer:
        out += 'washer-dryer-'
    if dishwasher:
        out += 'dishwasher-'
    if parking:
        out += 'parking-'
    if pool:
        out += 'pool-'
    if patio:
        out += 'patio-'

    # Remove the final '-' from the string
    out = out[0:len(out)-1]
    # Set the page we're searching on
    out += '/{page}/'.format(page=page)

    # Add bb if that exists
    if bb is not None:
        out += '?bb={bb}'.format(bb=bb)
    return out


# Provided a walkscore.com link to an address, this returns the walk, transit, and bike scores for that address
def get_scores(address):
    out = {
        'walk': 0,
        'transit': 0,
        'bike': 0
    }
    page = requests.get(address)

    # Check to make sure we actually connected to the address
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        scores = soup.find_all(class_='clearfix score-div')

        # Extract walk, transit, and bike scores from html
        # Should run 3 different times, once for each score
        for score in scores:
            subclass = score.find_all(class_='block-header-badge score-info-link')
            picture = subclass[0].find('img')
            text = picture.attrs['alt']

            if 'Walk Score' in text:
                if text[1] != ' ':
                    out['walk'] = text[0:3].strip()
                else:
                    out['walk'] = text[0]
            elif 'Transit Score' in text:
                if text[1] != ' ':
                    out['transit'] = text[0:3].strip()
                else:
                    out['transit'] = text[0]
            elif 'Bike Score' in text:
                if text[1] != ' ':
                    out['bike'] = text[0:3].strip()
                else:
                    out['bike'] = text[0]
    page.close()
    return out


# Takes a dict with information from apartments.com and appends walk/bike/transit score information
def append_walkscore(apartments):
    output = apartments
    for apartment in output:
        # Create url for walkscore.com and save it
        address = build_walkscore_link(street_address=apartment['streetAddress'],
                                       city=apartment['addressLocality'],
                                       state_code=apartment['addressRegion'],
                                       zip_code=apartment['postalCode'])
        apartment['walkscore_url'] = address

        # Go to walkscore link and save scores
        scores = get_scores(address)
        apartment['walk'] = scores['walk']
        apartment['transit'] = scores['transit']
        apartment['bike'] = scores['bike']
    return output


# Searches apartments.com and outputs to file
# Takes address, apartments.com bb search filter, as well as filters for amenities
# State must be state code
def get_apartments(city, state, start_page=1, bb=None, out_filename='output.csv', write_header=False,
                   under=2000, air_conditioning=True, washer_dryer=True, dishwasher=True,
                   parking=True, pool=True, patio=True, save_each_iteration=False):
    out = []
    page_index = start_page
    addresses_saved = 0
    link = build_apartments_link(city=city, state=state, page=start_page, bb=bb,
                                 under=under, air_conditioning=air_conditioning, washer_dryer=washer_dryer,
                                 dishwasher=dishwasher, parking=parking, pool=pool, patio=patio)
    page = requests.get(link, headers=header)

    soup = BeautifulSoup(page.content, 'html.parser')
    test = soup.find_all(class_='searchResults')

    try:
        total_addresses = int(soup.find_all(class_='searchResults')[0].contents[0].split()[3])
    except IndexError:
        total_addresses = 25

    while page.status_code == 200 and addresses_saved < total_addresses:
        print('Currently viewing data from link: {link}'.format(link=link))
        soup = BeautifulSoup(page.content, 'html.parser')
        data = json.loads(soup.find('script', type='application/ld+json').text)
        about = data['about']

        for entry in about:
            address = entry['Address']
            address['apartment_url'] = entry['url']
            address['image_url'] = entry['image']
            address['date_processed'] = datetime.today().strftime('%Y-%m-%d')
            out.append(address)

        page_index += 1
        link = build_apartments_link(city, state, page_index, bb=bb,
                                     under=under, air_conditioning=air_conditioning, washer_dryer=washer_dryer,
                                     dishwasher=dishwasher, parking=parking, pool=pool, patio=patio)
        page = requests.get(link, headers=header)

        if save_each_iteration:
            out = append_walkscore(out)
            with open(out_filename, newline='', mode='a') as output_file:
                writer = csv.DictWriter(output_file, out[0].keys())
                if write_header:
                    writer.writeheader()
                writer.writerows(out)

        addresses_saved += 25
        print("Finished iteration: {num_saved} addresses saved".format(num_saved=addresses_saved))
        time.sleep(10)

    if not save_each_iteration:
        out = append_walkscore(out)
        with open(out_filename, newline='', mode='a') as output_file:
            print('Output data to: {file}'.format(file=output_file))
            writer = csv.DictWriter(output_file, out[0].keys())
            if write_header:
                writer.writeheader()
            writer.writerows(out)
    return out


def main():
    today = datetime.today().strftime('%Y-%m-%d')
    out_filename = 'output\\{date} addresses.csv'.format(date=today)
    if os.path.isfile(out_filename):
        os.remove(out_filename)

    get_apartments(city='Austin', state='TX', out_filename=out_filename, write_header=True)
    get_apartments(city='Houston', state='TX', out_filename=out_filename, write_header=False)
    get_apartments(city='San-Antonio', state='TX', out_filename=out_filename)
    get_apartments(city='Corpus-Christi', state='TX', out_filename=out_filename)
    get_apartments(city='Chicago', state='IL', out_filename=out_filename)
    get_apartments(city='Philadelphia', state='PA', out_filename=out_filename)
    get_apartments(city='Washington', state='DC', out_filename=out_filename)
    get_apartments(city='Charlotte', state='NC', out_filename=out_filename)
    get_apartments(city='Raleigh', state='NC', out_filename=out_filename)
    get_apartments(city='Atlanta', state='GA', out_filename=out_filename)
    get_apartments(city='Seattle', state='WA', out_filename=out_filename, write_header=False)


main()