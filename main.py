import json
import time
from crypt import methods
from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scraper_find_classes(name):

    r1 = requests.get(f'https://reference.medscape.com/drug/{name}')
    soup = BeautifulSoup(r1.text, 'html.parser')

    simple_name = soup.find('span', {'class': 'drugbrandname'}).get_text()

    sub_category = soup.find('div', {'id': 'maincolboxdrugdbheader'}).ul.li.a.get_text()
    sub_category = sub_category.replace(' ', '-').lower()

    r2 = requests.get(f'https://reference.medscape.com/drugs/{sub_category}')
    soup2 = BeautifulSoup(r2.text, 'html.parser')

    main_category = soup2.find('div', {'id': 'byclassbc'}).find_all('a')[1].get_text()

    response = {}

    response['data'] = {'name': simple_name, 'class': main_category}

    return response

if __name__ == "__main__":
    name = 'accupril-quinapril-342330'

    print(scraper_find_classes(name))