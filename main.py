import json
import time
from crypt import methods
from unicodedata import category
from flask import Flask, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def find_class(name):

    r1 = requests.get(f'https://reference.medscape.com/drug/{name}')
    soup = BeautifulSoup(r1.text, 'html.parser')

    brand_name = soup.find('span', {'class': 'drugbrandname'}).find('span').next_sibling

    sub_category = soup.find('div', {'id': 'maincolboxdrugdbheader'}).ul.li.a.get_text()
    sub_category = sub_category.replace(' ', '-').lower()

    r2 = requests.get(f'https://reference.medscape.com/drugs/{sub_category}')
    soup2 = BeautifulSoup(r2.text, 'html.parser')

    main_category = soup2.find('div', {'id': 'byclassbc'}).find_all('a')[1].get_text()

    response = {}

    response['data'] = {'name': brand_name, 'class': main_category}

    return response

def find_categories():

  categories = []
  r1 = requests.get('https://reference.medscape.com/drugs')
  soup = BeautifulSoup(r1.text, 'html.parser')

  list = soup.find('div', {'id': 'drugdbmain2'}).ul.findAll('li')

  for category in list:
    category_name = category.a.get_text()
    categories.append(category_name)
  
  return categories

if __name__ == "__main__":
  categories = find_categories()
  for category in categories:
    print(category)