# RHTE-SWAPI
Red Hat Technical Assessment - Star Wars API

### Requirements<hr>
* Py3.6+ - recommended to add pythong to `PATH` if using Windows (this assessment was shamefully completed using Win10 64x on Command Prompt)
** mysql-connector
** requests
** `python -m pip install mysql-connector requests`



### Notes<hr>
* This assessment was completed using 64x Windows 10, so all directions will be more detailed for windows users. The consolation prize for non-Windows users is a prize in itself.
* We're doing this insecurely. If you have time, and if you want to extend this set of test responses or create an app out of this somehow, it's recommended you take a bit longer working on security (e.g. host your MySQL instance using a different port, don't use `--initialize-insecure`, format your queries using parameters and not with straight `.format()` to avoid sql injection, etc)
* `~/` will be used as a placeholder for the folder/directory that hosts all of the necessary folders.

### Steps<hr>
1. Download and install MySQL: https://dev.mysql.com/downloads/mysql/
    - https://dev.mysql.com/downloads/file/?id=484900 for the direct download link. Below the big, basically adware, buttons is a "No thanks, just start my downloads" link. Click that.
    - The above link downloads something called a `noinstall` ZIP Archive. Drop the zip file wherever and then extract it into the desired location (f. ex. `~/`).
      - NOTE: I do not know if spaces in the destination path matter, but I've had issues with that in the past, because, you know, Windows, so I am putting it somewhere where there are no spaces in the target directory.
    - At this point my directory has two sub-folders: RHTE-SWAPI and mysql-8.0.15-winx64
    - Navigate to the MySQL directory (`~/mysql-8.0.15-win64x`) in your CLI of choice and run the command `~/mysql-8.0.15-win64x> bin\mysqld --initialize-insecure --console`. A bunch of stuff will print out and then you'll be able to continue.
     - security note: this creates the root user without a password
    - run `~/mysql-8.0.15-win64x> bin\mysqld --console` to spin up the server. This should create a mysql server instance running LocalHost:[some port, probably 3306]. This also locks up the CLI that you used to spin it up, so open another one.
    - Open another console, navigate to the mysql server directory, and run the command `~/mysql-8.0.15-win64x>bin\mysql -u root --skip-password`
    - Run the command `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<yourpasswordhere>'`
    - Leave the server spinning. We're about to use it.
    - For now, we'll just use the default `mysql` database and dump everything there.
    - At this point you can close the mysql console and continue.
2. Download and install the required packages `~/>python -m pip install requests mysql-connector`:
    - requests
    - mysql-connector
3. Open and edit `table_gen.py` in your text editor of choice.
    - Fill out the MySQL Connector args in `conn` using the appropriate arguments.
    - `n` is the number of characters to load. Default 15.
    - `distinct` is if we want `n` distinct characters. Setting `distinct` to `False` will allow the RNG to pick the same character more than once. Since `dim_character`, `dim_film`, and `dim_appearance` are de-duplicated by design, this will just load in  `<= n` characters, depending on if one or more characters were chosen more than once (e.g. if a character is picked `n` times, then there will only be one character instance loaded into `dim_character`, `dim_film`, and `fact_appearance`.) Insert statements are also de-duplicated, so `inter_` tables _should_ have unique loads.
4. Run the file using your python interpreter (assuming you've installed the requirements, mysql-connector and requests):
    - `~/>python.exe table_gen.py` if you're in the same directory
    - NOTES:
      - the statements that create `dim_character`, `dim_film`, and `fact_appearance` are all idempotent. This script can be run as many times as you want and there should only be one row per film, character, and film/character combo in each table, respectively.
      - `inter_*` tables are not due to assessment constraints (`CREATE` `INSERT` `SELECT`)
    - run `~/mysql-8.0.15-win64x> bin\mysqldump -u root -p mysql --no-data > ../db.sql` to dump schema information into your folder.
5. After you're satisfied with your tables, export them for later.
6. Run `task_one.py` using your python interpreter (assuming you've installed the requirements, mysql-connector)
    - `~>python.exe task_one.py`
    - This should print out three different printouts: one that just prints out the resulting dictionary, one that pprints the resulting dictionary, and then one that's formatted using a for loop and string formatting.
7. (OPTIONAL - Task 1.5) run `schema_scrape` to get `.schemas`, a file that outlines some of the major object schemas
8. Run `task_two.py` using your python interpreter (assuming you've installed the requirements, requests)
   - `task_two.py` writes the result to `ANewHopeDetail.json` and prints the output into the console using pprint.
   - Note: Meters and Centimeters are converted to feet, kilograms are converted to pounds.
