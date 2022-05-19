import json
from googletrans import Translator

translator = Translator()
data = json.load(open('active_principles.json'))

info = json.dumps(data, ensure_ascii=False, indent=4).encode('utf8')

translate = translator.translate(info, src='en', dest='es')
# text = translate.text
# dict = json.loads(text)

with open('active_principles_es.json', 'w', encoding='utf8') as f:
    # json.dump(info, f, indent=4)
    f.write(info.decode())

with open('active_principles_es.json') as data_file:
  data = json.load(data_file)
  for key, value in data.items():
    key = translator.translate(key, src='en', dest='es')
    key = key.text
