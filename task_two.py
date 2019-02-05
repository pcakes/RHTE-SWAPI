"""This is an embarassing mess but I'm pretty sure it'll work for any film."""

import json
import pprint
import requests

def s_to_f(metric):
  if metric in ['unknown', 'n/a']:
    return None
  else:
    return float(metric.replace(',', '').replace('.', ''))


def reference(ref, obj_type):
  item = requests.get(ref).json()
  rm = list()
  for prop in item:
  # Remove properties of type array or if `http://swapi.co/api/` is a substring.
    if (schemas[obj_type]['properties'][prop]['type'] == 'array'
        or part in str(item[prop]).replace('https://', 'http://')):
      rm.append(prop)
    else:
    # Convert lengths, heights
      if 'in centimeters' in schemas[obj_type]['properties'][prop]['description']:
        item[prop] = item[prop] if not s_to_f(item[prop]) else s_to_f(item[prop]) * 0.03281
      elif 'in meters' in schemas[obj_type]['properties'][prop]['description']:
        item[prop] = item[prop] if not s_to_f(item[prop]) else s_to_f(item[prop]) * 3.28084
      elif 'in kilograms' in schemas[obj_type]['properties'][prop]['description']:
        item[prop] = item[prop] if not s_to_f(item[prop]) else s_to_f(item[prop]) * 2.20462
      else:
        continue
  for r in rm:
    item.pop(r)
  return item


part = 'http://swapi.co/api/'

# Schemas
schemas = dict()
# get schemas
schemas['characters'] = requests.get(part + 'people/schema').json()
schemas['starships'] = requests.get(part + 'starships/schema').json()
schemas['planets'] = requests.get(part + 'planets/schema').json()
schemas['vehicles'] = requests.get(part + 'vehicles/schema').json()
schemas['species'] = requests.get(part + 'species/schema').json()
schemas['films'] = requests.get(part + 'films/schema').json()


film_id = 1
req = part + 'films/{FILM_ID}/'.format(FILM_ID=film_id)

film = requests.get(req).json()

result = dict()

for property in film:
  if property in schemas:
    tre = [reference(k, property) for k in film[property]]
    film[property] = tre
  else:
    # Convert lengths, heights
    if 'in centimeters' in schemas['films']['properties'][property]['description']:
      film[prop] = film[prop] if not s_to_f(film[prop]) else s_to_f(film[prop]) * 0.03281
    elif 'in meters' in schemas['films']['properties'][property]['description']:
      item[prop] = film[prop] if not s_to_f(film[prop]) else s_to_f(film[prop]) * 3.28084
    elif 'in kilograms' in schemas['films']['properties'][property]['description']:
      item[prop] = film[prop] if not s_to_f(film[prop]) else s_to_f(film[prop]) * 2.20462
    else:
      continue


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(film)
with open('ANewHopeDetail.json', 'w') as f:
  json.dump(film, f)