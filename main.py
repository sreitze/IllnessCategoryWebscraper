from crypt import methods
from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import csv

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

def find_active_principles(category_raw, sub_category):
  
  active_principles = []
  category = translate(category_raw)

  r1 = requests.get(f'https://reference.medscape.com/drugs/{category}')
  soup = BeautifulSoup(r1.text, 'html.parser')

  link = soup.find('div', {'id': 'drugdbmain2'}).ul.find('li', string=sub_category).a.get('href')
  r2 = requests.get(link)
  soup2 = BeautifulSoup(r2.text, 'html.parser')
  list = soup2.find('div', {'id': 'drugdbmain2'}).ul.findAll('li')

  for l in list:
    link = l.a.get('href')
    r = requests.get(link)
    s = BeautifulSoup(r.text, 'html.parser')
    box = s.find('div', {'id': "maincolboxdrugdbheader"})
    if box is not None:
      active_principle = box.h1.find('span', {'class': 'drug_suffix'}).previousSibling.get_text()
      active_principles.append([str(active_principle), category_raw])

  return active_principles

def translate(category):
  if '&' in category:
    category = category.split(' & ')
    category = '-'.join(category).replace(' ', '-')
  elif ' ' in category:
    category = category.replace(' ', '-')
  return category.replace("'", "").lower()

if __name__ == "__main__":
  active_principles = []
  categories = find_categories()
  sub_categories = find_sub_categories(categories[0])
  active_principles = find_active_principles(categories[0], sub_categories[2])
  # for category in categories:
  #   sub_categories = find_sub_categories(category)
  #   for sub_category in sub_categories:
  #     active_principles.append(find_active_principles(category, sub_category))

  with open('active_principles.csv', 'a') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(['name', 'category'])
    writer.writerows(active_principles)

  # The idea is to loop through all the categories and it's sub-categories to get each active principle
  # and connect it to its general category through a csv or JSON file