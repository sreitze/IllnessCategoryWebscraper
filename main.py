import json
import time
from scaper import Scraper

if __name__ == "__main__":
  scraper = Scraper()
  active_principles = []
  translate = True
  
  categories = ['Allergy & Cold', 'Anesthetics', 'Antidotes', 'Antimicrobials', 
                'Blood Components', 'Cardiovascular', 'Critical Care', 'Dental & Oral Care', 
                'Dermatologics', 'Gastrointestinal', 'Hematologics', 'Herbals & Supplements', 
                'Imaging Agents', 'Immunologics', 'Metabolic & Endocrine', 'Neurologics', 
                'Nutritionals', 'Oncology', 'Ophthalmics', 'Otics', 
                'Pain Management', 'Psychiatrics', 'Pulmonary', 'Rheumatologics', 
                'Urologics', 'Vaccinations', "Women's Health & Reproduction"]
  
  categorias = ['Alergia y Resfrío', 'Anestésicos', 'Antídotos', 'Antimicrobianos',
                'Componentes de la sangre', 'Cardiovascular', 'Cuidado crítico', 'Cuidado bucal y dental',
                'Dermatológicos', 'Gastrointestinal', 'Hematológicos', 'Hierbas y Suplementos',
                'Agentes de imagen', 'Inmunológicos', 'Metabólico y Endocrino', 'Neurológicos',
                'Nutricionales', 'Oncología', 'Oftalmología', 'Óptica', 
                'El manejo del dolor', 'Psiquiatría', 'Pulmonar', 'Reumatológicos',
                'Urológicos', 'Vacunas', 'Salud y reproducción de la mujer']
                
  # PARA CORRER TODOS LOS PRINCIPIOS ACTIVOS, DESCOMENTAR

  c = 0
  while c < 25:
    for category in categories[c:c+2]:
      checked = []
      sub_categories = scraper.find_sub_categories(category)
      for sub_category in sub_categories:
        category_es = categorias[categories.index(category)]
        active_principles, checked = scraper.find_active_principles(category, category_es, sub_category, active_principles, checked, translate)
      if translate:
        time.sleep(2)
    c += 1
    if translate:
      time.sleep(120)

  # PARA CORRER SOLO UNA CATEGORIA COMPLETA, DESCOMENTAR

  sub_categories = scraper.find_sub_categories(categories[26])
  checked = []
  for sub_category in sub_categories:
    active_principles, checked = scraper.find_active_principles(categories[26], categorias[26], sub_category, active_principles, checked, translate)

  # PARA CORRER UNA SUB-CATEGORIA, DESCOMENTAR

  # sub_categories = scraper.find_sub_categories(categories[0])
  # active_principles = scraper.find_active_principles(categories[0], categorias[0], sub_categories[0], active_principles)
  
  dictionary = dict(active_principles)

  json_dict = json.dumps(dictionary, ensure_ascii=False, indent=4).encode('utf8')

  with open('active_principles.json', 'w', encoding='utf8') as f:
    # json.dump(dictionary, f, indent=4)
    f.write(json_dict.decode())

  # The idea is to loop through all the categories and it's sub-categories to get each active principle
  # and connect it to its general category through a JSON file