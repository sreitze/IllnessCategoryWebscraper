import requests
import time
from bs4 import BeautifulSoup
from googletrans import Translator

class Scraper:

  def __init__(self):
    self.translator = Translator()

  def translate(self, category):
    if '&' in category:
      category = category.split(' & ')
      category = '-'.join(category).replace(' ', '-')
    elif ' ' in category:
      category = category.replace(' ', '-')
    return category.replace("'", "").lower()

  def find_sub_categories(self, category):

    category = self.translate(category)
    sub_categories = []
    r1 = requests.get(f'https://reference.medscape.com/drugs/{category}')
    soup = BeautifulSoup(r1.text, 'html.parser')

    list = soup.find('div', {'id': 'drugdbmain2'}).ul.findAll('li')

    for sub_category in list:
      sub_category_name = sub_category.a.get_text()
      sub_categories.append(sub_category_name)
    
    return sub_categories

  def find_active_principles(self, category_raw, category_es, sub_category, active_principles, checked, translate):
    category = self.translate(category_raw)

    r1 = requests.get(f'https://reference.medscape.com/drugs/{category}')
    soup = BeautifulSoup(r1.text, 'html.parser')

    container = soup.find('div', {'id': 'drugdbmain2'})
    if container is not None:
      link = container.ul.find('li', string=sub_category).a.get('href')
      r2 = requests.get(link)
      soup2 = BeautifulSoup(r2.text, 'html.parser')
      box = soup2.find('div', {'id': 'drugdbmain2'})
      if box is not None:
        list_sub_categories = box.ul.findAll('li')

        for l in list_sub_categories:
          link_active_principle = l.a.get('href')
          r = requests.get(link_active_principle)
          s = BeautifulSoup(r.text, 'html.parser')
          box = s.find('div', {'id': "maincolboxdrugdbheader"})
          if box is not None:
            active_principle = box.h1.find('span', {'class': 'drug_suffix'}).previousSibling.get_text()
            if active_principle is not None:
              if active_principle not in checked:
                checked.append(active_principle)
                if translate:
                  translated = self.translator.translate(active_principle, src='en', dest='es')
                  print(translated.text, category_es)
                  active_principles.append((translated.text, category_es))
                else:
                  active_principles.append((active_principle, category_raw))
      else:
        box = soup2.find('div', {'id': "maincolboxdrugdbheader"})
        if box is not None:
          active_principle = box.h1.find('span', {'class': 'drug_suffix'}).previousSibling.get_text()
          if active_principle is not None:
            if active_principle not in checked:
              checked.append(active_principle)
              if translate:
                translated = self.translator.translate(active_principle, src='en', dest='es')
                print(translated.text, category_es)
                active_principles.append((translated.text, category_es))
              else:
                active_principles.append((active_principle, category_raw))

    return active_principles, checked