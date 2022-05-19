import json
from scaper import Scraper

if __name__ == "__main__":
  scraper = Scraper()
  active_principles = []
  categories = scraper.find_categories()
                
  for category in categories:
    sub_categories = scraper.find_sub_categories(category)
    for sub_category in sub_categories:
      active_principles = scraper.find_active_principles(category, sub_category, active_principles)
  
  dictionary = dict(active_principles)

  with open('active_principles.json', 'w') as f:
    json.dump(dictionary, f, indent=4)

  # The idea is to loop through all the categories and it's sub-categories to get each active principle
  # and connect it to its general category through a JSON file