import json
import time
from scaper import Scraper

if __name__ == "__main__":
  scraper = Scraper()
  active_principles = []
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
                
  for category in categories:
    sub_categories = scraper.find_sub_categories(category)
    for sub_category in sub_categories:
      category_es = categorias[categories.index(category)]
      active_principles = scraper.find_active_principles(category, category_es, sub_category, active_principles)
      time.sleep(2)

  # sub_categories = scraper.find_sub_categories(categories[14])
  # for sub_category in sub_categories:
  #   active_principles = scraper.find_active_principles(categories[14], categorias[14], sub_category, active_principles)
  
  dictionary = dict(active_principles)

  json_dict = json.dumps(dictionary, ensure_ascii=False, indent=4).encode('utf8')

  with open('active_principles.json', 'w', encoding='utf8') as f:
    # json.dump(dictionary, f, indent=4)
    f.write(json_dict.decode())

  # The idea is to loop through all the categories and it's sub-categories to get each active principle
  # and connect it to its general category through a JSON file