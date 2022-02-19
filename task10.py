
import json
from pprint import pprint

with open("task4.json", "r") as f:
    object = json.load(f)

directors = []
for data in object:
    for director in data['director']:
        if director not in directors:
            directors.append(director)

languages_with_director = []
for director in directors:
    langs = {}
    for data in object:
        if director in data['director']:
            for lang in data['language']:
                if lang not in langs:
                    langs[lang] = 1
                else:
                    langs[lang] += 1
    languages_with_director.append({director:langs})

with open("task10.json", 'w') as f:
    json.dump(languages_with_director, f, indent=4)
