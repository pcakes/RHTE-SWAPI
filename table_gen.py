"""Using only `SELECT`, `INSERT`, AND `CREATE`, create tables that can be used for the technical
assessment.

Since we can't drop, truncate, or delete, `inter_` is going to grow, but this script will ensure
duplicate rows aren't entered into the final tables.

Steps:
1. Create tables if not exists:
    a. dim_character, dim_film, fact_appearance
2. Populate inter_dim_ and inter_fact_ tables.
3. Insert into final tables those values that don't exist already in the final table.
    a. using inter_ and the final table, INSERT DISTINCT values where the values are in the inter_
       table and not in the final table

Next steps:
1. Generalize to take in an entire arbitrary object. Each url has the pattern
   "swapi.co/api/{object}/{id}/"
    a. Create dim_ and inter_dim_ tables for each object
    b. Expand all dim_ and inter_dim_ tables to include traits with non-list values like metrics
    c. Create fact_ and inter_fact_ tables for traits with listlike values (relational traits)
"""

import json
import mysql.connector
import random
import requests

# Misc / Utility
def get_id(rurl):
  r"""Returns the id for the given object"""
  return int(rurl.split('/')[-2].replace('/', ''))


# Create all necessary tables
def create_tables(tables):
  r"""Creates inter_ and final tables for each table in `tables` if they don't exist.
  PARAMETERS
  ----------
  tables : dict
    keys are final table names (e.g. `dim_film`), elements are table field definitions.
  EXAMPLE
  ----------
  tables = {'dim_film': {'id': 'int', 'name': 'text'},
            'dim_character': {'id': 'int', 'name': 'text'},
            'fact_appearance': {'character_id': 'int', 'film_id': 'int'}}
  RETURNS
  ----------
  str
    single command to create all tables that don't exist.
  """
  stm = "CREATE TABLE IF NOT EXISTS {TABLE} ({FIELDS});"
  lst_q = list()
  for table in tables:
    # Formatting the table types using the schema.
    # separate each '`name` `type`' using a comma and a newline char (log-reader's sake)
    ifastm = '\n  ,'.join(' '.join([k, tables[table][k]]) for k in tables[table])
    lst_q += [stm.format(TABLE=i + table, FIELDS=ifastm) for i in ['inter_', '']]
  return lst_q


def insert_stm(table, values):
  r"""Creates an insert statement for the given values to the target table.
  PARAMETERS
  ----------
  table : str
    target table name
  values : list
    list of values to insert into `table`
  RETURNS
  ----------
  str
  """
  stm = "INSERT INTO inter_{TABLE} VALUES ({VALUES});"
  return stm.format(TABLE=table, VALUES=', '.join(str(e) for e in values))


def final_table_stm(table, schema):
  r"""Generates SQL statement that updates the final table to discard values already in the
  table.
  PARAMETERS
  ----------
  table : str
    target table name
  schema : dict
    elements are field names, keys are data types. Keys aren't used, but layout needed for
    iteration
  """
  sql = """
INSERT INTO {TABLE} (
  SELECT DISTINCT
    {FIELDS}
  FROM (
    SELECT DISTINCT
      i.*
    FROM (
      SELECT DISTINCT
        {FIELDS}
      FROM
        inter_{TABLE}
      ) i
    LEFT JOIN (
      SELECT DISTINCT
        {FIELDS}
      FROM
        {TABLE}
      ) f
      ON {JCLAUSE}
    WHERE
      f.{X} IS NULL
    ORDER BY
      1 ASC
  ) x
);
  """
  jclause = ' AND '.join('i.{} = f.{}'.format(i, i) for i in schema[table])
  fields = ', '.join(i for i in schema[table])
  x = list(schema[table].keys())[0]
  return sql.format(TABLE=table, FIELDS=fields, JCLAUSE=jclause, X=x)

# Connection string
conn = mysql.connector.connect(
  host="localhost",
  port=3306,
  user="root",
  password="adminlol",
  database="mysql",
  auth_plugin='mysql_native_password'
)
cursor = conn.cursor()

# Set number of characters to add
n = 15
distinct = True
# start with empty set of persons
persons = set() if distinct else list()
# While persons has less population than the target population, add a random person id
while len(persons) < n:
  if distinct:
    persons.add(random.randint(1, 87))
  else:
    persons.append(random.randint(1, 87))

persons = set(e for e in persons)

# Request skeleton
req = 'http://swapi.co/api/{OBJ}/{RN}/'

# Appearances dict. To be filled out with character ids and sets on what films they appeared
# in
appearances = dict()

tables = {
  'dim_character': {'id': 'int', 'name': 'text'},
  'dim_film': {'id': 'int', 'name': 'text'},
  'fact_appearance': {'character_id': 'int', 'film_id': 'int'}
}

create = create_tables(tables)

characters = {i: requests.get(req.format(OBJ='people', RN=i)).json() for i in persons}
missing = [i for i in characters if 'url' not in characters[i]]
characters = [characters[i] for i in characters if i not in missing]
print('Missing Persons: {i}\nSkipping persons {i}.'.format(i=missing))

# inter_dim_character insert statements
idcstm = set()

# inter_dim_film insert statements
idfstm = set()

# inter_fact_appearance insert statements
ifastm = set()

# insert into tables statements
iitstm = set()

# Films
films = set()

# Character inserts
for character in characters:
  # character id
  iden = get_id(character['url'])
  # character name
  name = character['name']
  # insert character id and name into inter_dim_character
  stm = insert_stm('dim_character', [iden, "'" + name + "'"])
  # add character insert statement to idcstm
  idcstm.add(stm)

  # Not sure if there's a list of films on every character. Not advocating for or against fan fic
  # cannon here.
  if 'films' in character:
    # for each film
    for film in character['films']:
      # get the film id
      fid = get_id(film)
      # add the character appearance for inter_fact_appearance
      stm = insert_stm('fact_appearance', [iden, fid])
      ifastm.add(stm)
      # Save update the set of films for inter_dim_film statements
      films.add(film)

for film in films:
  # film id
  iden = get_id(film)
  # Get film object
  obj = requests.get(req.format(OBJ='films', RN=iden)).json()
  # Add insert statement for inter_dim_film
  idfstm.add(insert_stm('dim_film', [iden, "'" + obj['title'] + "'"]))

for table in tables:
  iitstm.add(final_table_stm(table, tables))

for stms in [create, idcstm, idfstm, ifastm, iitstm]:
  for sql in stms:
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()
