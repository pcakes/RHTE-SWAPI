"""When called, output something like this into the console:
[
  {
    "Film": "The Empire Strikes Back",
      "Character":
      [
        "Luke Skywalker",
        "C-3P0",
        "Han Solo",
        "R2-D2",
        "Darth Vader"
      ]
  },
  {
    "Film": "Return of the Jedi",
      "Character":
      [
        "Luke Skywalker",
        "C-3P0",
        "Han Solo",
        "R2-D2",
        "Darth Vader"
      ]
  }
]
"""
import mysql.connector

# Connection string
conn = mysql.connector.connect(
  host="localhost",
  port=3306,
  user="root",
  password="admin",
  database="mysql",
  auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

sql = """
SELECT
  f.name
  ,c.name
FROM
  dim_character c
JOIN
  fact_appearance fa
  ON fa.character_id = c.id
JOIN
  dim_film f
  ON f.id = fa.film_id
"""

# Get results
cursor.execute(sql)

data = [k for k in cursor]
# create a list of dictionaries where keys are "film" and "character" and elements to those keys
# are the film name and the characters that appear in the film, respectively.
result = [{"film": k, "character": [e[1] for e in data if e[0] == k]}
          for k in set(i[0] for i in data)]
# Technically what was asked for: "like"
print('Ugly result (something "like" what was shown):\n', result)

# Closer result, using pretty print
import pprint
pp = pprint.PrettyPrinter(indent=4)
print('\nslightly prettier:')
pp.pprint(result)

# I'm not sure why I did this, but here it is.
s = "["
fs = '\n    "film": {f},\n'
cs = '    "character":\n    [\n      "{c}"\n    ]\n  '

print("\nAhhh, that's the stuff:")
for k in result:
  if s == '[':
    s += '\n'
  else:
    s += ',\n'
  s += '  {' + fs.format(f=k['film'])
  s += cs.format(c='",\n      "'.join(k['character'])) + '}'
s += ']'
print(s)