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

def find_sub_categories(category):

  category = translate(category)
  sub_categories = []
  r1 = requests.get(f'https://reference.medscape.com/drugs/{category}')
  soup = BeautifulSoup(r1.text, 'html.parser')

  list = soup.find('div', {'id': 'drugdbmain2'}).ul.findAll('li')

  for sub_category in list:
    sub_category_name = sub_category.a.get_text()
    sub_categories.append(sub_category_name)
  
  return sub_categories

def find_active_principles(category, sub_category):
  
  active_principles = []
  category = translate(category)
  r1 = requests.get(f'https://reference.medscape.com/drugs/{category}')
  soup = BeautifulSoup(r1.text, 'html.parser')

  link = soup.find('div', {'id': 'drugdbmain2'}).ul.find('li', string=sub_category).a.get('href')

  r2 = requests.get(link)
  soup2 = BeautifulSoup(r2.text, 'html.parser')
  list = soup2.find('div', {'id': 'drugdbmain2'}).ul.findAll('li')
  for l in list:
    r = requests.get(l.a.get('href'))
    s = BeautifulSoup(r.text, 'html.parser')
    active_principle = s.find('div', {'id': 'maincolboxdrugdbheader'}).h1.span.get_text()
    active_principles.append(active_principle)

  return active_principles

def translate(category):
  if '&' in category:
    category = category.split(' & ')
    category = '-'.join(category).replace(' ', '-')
  elif ' ' in category:
    category = category.replace(' ', '-')
  return category.replace("'", "").lower()

if __name__ == "__main__":
  categories = find_categories()
  sub_categories = find_sub_categories(categories[0])
  print(find_active_principles(categories[0], sub_categories[4]))