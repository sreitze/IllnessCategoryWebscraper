import json
from googletrans import Translator

translator = Translator()
data = json.load(open('active_principles.json'))
string = json.dumps(data)

translate = translator.translate(string, src='en', dest='es')
text = translate.text
dict = json.loads(text)

with open('active_principles_es.json', 'w') as f:
    json.dump(dict, f, indent=4)