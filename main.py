from crypt import methods
import requests
from bs4 import BeautifulSoup
import json

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

def find_active_principles(category_raw, sub_category, active_principles):

  category = translate(category_raw)

  r1 = requests.get(f'https://reference.medscape.com/drugs/{category}')
  soup = BeautifulSoup(r1.text, 'html.parser')

  link = soup.find('div', {'id': 'drugdbmain2'}).ul.find('li', string=sub_category).a.get('href')
  r2 = requests.get(link)
  soup2 = BeautifulSoup(r2.text, 'html.parser')
  box = soup2.find('div', {'id': 'drugdbmain2'})
  if box is not None:
    list_sub_categories = box.ul.findAll('li')

    for l in list_sub_categories:
      link = l.a.get('href')
      r = requests.get(link)
      s = BeautifulSoup(r.text, 'html.parser')
      box = s.find('div', {'id': "maincolboxdrugdbheader"})
      if box is not None:
        active_principle = box.h1.find('span', {'class': 'drug_suffix'}).previousSibling.get_text()
        active_principles.append((active_principle, category_raw))
  else:
    box = soup2.find('div', {'id': "maincolboxdrugdbheader"})
    if box is not None:
      active_principle = box.h1.find('span', {'class': 'drug_suffix'}).previousSibling.get_text()
      active_principles.append((active_principle, category_raw))

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
  # sub_categories = find_sub_categories(categories[0])
  # active_principles = find_active_principles(categories[0], sub_categories[0])
  # for category in categories:
  sub_categories = find_sub_categories(categories[0])
  for sub_category in sub_categories:
    active_principles = find_active_principles(categories[0], sub_category, active_principles)
  dictionary = dict(active_principles)

  with open('active_principles.json', 'w') as f:
    json.dump(dictionary, f, indent=4)

  # The idea is to loop through all the categories and it's sub-categories to get each active principle
  # and connect it to its general category through a JSON file