import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)
# Let's just take a look at schemas to figure out what to expect for task_two
print('People')
pp.pprint(requests.get('http://swapi.co/api/people/schema').json())

print('Starships')
pp.pprint(requests.get('http://swapi.co/api/starships/schema').json())

print('Planets')
pp.pprint(requests.get('http://swapi.co/api/planets/schema').json())

print('Planets')
pp.pprint(requests.get('http://swapi.co/api/vehicles/schema').json())

print('Species')
pp.pprint(requests.get('http://swapi.co/api/species/schema').json())

print('Films')
pp.pprint(requests.get('http://swapi.co/api/films/schema').json())