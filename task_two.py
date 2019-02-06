"""This is an embarassing mess but I'm pretty sure it'll work for any film."""

import json
import pprint
import requests
import time

def s_to_f(metric):
  r"""Takes what we expect to be a float value (some physical metric like height or weight)
  and attempts to convert it to float. Some assumed-to-be metric values are labeled as 'unknown'
  or 'n/a', so we return None and deal with those in line using a `x if not x else s_to_f(x)`
  """
  if metric in ['unknown', 'n/a']:
    return None
  else:
    return float(metric.replace(',', '').replace('.', ''))


def reference(ref, obj_type):
  r"""this one's kind of a doozy. First, take the reference, e.g. http://swapi.co/species/n/.
  Then call the object using `requests`. dump it into a dictionary. For each property (key in the
  dict), if the property is an array remove it, if the property has an api reference in it, remove
  it, if the property has a metric-sort-of description ("in centimeters" or "in kilograms"), wrap
  a switch around it and convert it to the standard equivalent (cm/m -> ft, Kg -> lb).
  
  Return dictionary, which later boils down to replacing the api reference with the object's
  properties, sans cross references.
  """
  # Call reference (character, species, starship, etc)
  item = requests.get(ref).json()
  # create unpopulated list of "things to remove"
  rm = list()
  # for property in the object/item
  for prop in item:
  # flag properties of type array or reference as "remove"
    if (schemas[obj_type]['properties'][prop]['type'] == 'array'
    # `part` is saved in the beginning of the code. it's basically the base url for swapi
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
      # don't care about anything else, hopefully.
        continue
  # remove all things that are flagged for removal
  for r in rm:
    item.pop(r)
  # Return the mutated API call result
  return item

# Prepare pretty-print console check
pp = pprint.PrettyPrinter(indent=4)

# Save for later.
part = 'http://swapi.co/api/'

# Schemas
schemas = dict()
# get schemas for iteration/reference
schemas['characters'] = requests.get(part + 'people/schema').json()
schemas['starships'] = requests.get(part + 'starships/schema').json()
schemas['planets'] = requests.get(part + 'planets/schema').json()
schemas['vehicles'] = requests.get(part + 'vehicles/schema').json()
schemas['species'] = requests.get(part + 'species/schema').json()
schemas['films'] = requests.get(part + 'films/schema').json()

# film to do this for
film_id = 1
req = part + 'films/{FILM_ID}/'.format(FILM_ID=film_id)

# Get film properties
film = requests.get(req).json()
# print original for visual checking (count printed references to species, characters, etc)
pp.pprint(film)

# Prepare result dumping ground
result = dict()

# for each property in the film
for property in film:
  # If the property is in our set of schemas
  if property in schemas:
    # extend the reference to be the actually-referenced object, removing cross-references
    # and converting length/weight metrics.
    tre = [reference(k, property) for k in film[property]]
    film[property] = tre
  else:
    # Convert lengths, heights in the main film object if they exist.
    # This can be in a function and can be recursive somehow, I'm sure
    if 'in centimeters' in schemas['films']['properties'][property]['description']:
      film[prop] = film[prop] if not s_to_f(film[prop]) else s_to_f(film[prop]) * 0.03281
    elif 'in meters' in schemas['films']['properties'][property]['description']:
      item[prop] = film[prop] if not s_to_f(film[prop]) else s_to_f(film[prop]) * 3.28084
    elif 'in kilograms' in schemas['films']['properties'][property]['description']:
      item[prop] = film[prop] if not s_to_f(film[prop]) else s_to_f(film[prop]) * 2.20462
    else:
      continue

# Print the mutated film for visual checking (counts)
pp.pprint(film)
# "So what was your best run? Oh, it was '2019-02-05T19:03:23Z.38002.'
# '2019-02-05T19:07:01Z.118000' was a bust, so I had to go back. Why?"
now = time.strftime('%Y%m%d%H%M')
with open('{}_{}_detail_{}.json'.format(film_id, film['title'], now), 'w') as f:
  json.dump(film, f)

# Sometimes you just gotta follow the directions
with open('task_two.json'.format(film_id, film['title'], now), 'w') as f:
  json.dump(film, f)