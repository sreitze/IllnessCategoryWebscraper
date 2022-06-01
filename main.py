import json
from googletrans import Translator
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
      active_principles = scraper.find_active_principles(category, 'hola', sub_category, active_principles)

  # sub_categories = scraper.find_sub_categories(categories[0])
  # active_principles = scraper.find_active_principles(categories[0], categorias[0], sub_categories[1], active_principles)
  
  dictionary = dict(active_principles)

  with open('active_principles.json', 'w') as f:
    json.dump(dictionary, f, indent=4)

  # The idea is to loop through all the categories and it's sub-categories to get each active principle
  # and connect it to its general category through a JSON file