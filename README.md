# RHTE-SWAPI
Red Hat Technical Assessment - Star Wars API

### Notes<hr>
* This assessment was completed using 64x Windows 10, so all directions will be more detailed for windows users. The consolation prize for non-Windows users is a prize in itself.
* We're doing this insecurely. If you have time, and if you want to extend this set of test responses, I recommend taking a few more secure steps
* Since I'm on a roll admitting embarrassing facts, I'll go ahead and admit that I'm using Windows Command Line for this. Use your CLI of choice.
* ~/ from here on out will be whatever directory you're using to host everything you need. In my case, it's C:\Users\Pclarke\Desktop\misc\
* We're using python 3. Install it wherever. I've added it to my PATH variable, so I just need to run `python.exe [script]`, but if you haven't done/can't do this, replace `python.exe` with the full path pointing towards the `python.exe` you wish to use.

### Steps<hr>
1. Download and install MySQL: https://dev.mysql.com/downloads/mysql/
    a. https://dev.mysql.com/downloads/file/?id=484900 for the direct download link.
    b. The above link downloads something called a `noinstall` ZIP Archive. Drop the zip file wherever and then extract it into the desired location.
        i. NOTE: I do not know if spaces in the destination path matter, but I've had issues with that in the past, because, you know, Windows, so I am putting it somewhere where there are no spaces in the target directory.
    c. At this point my directory has two sub-folders: RHTE-SWAPI and mysql-8.0.15-winx64
    d. Navigate to the MySQL directory (~/mysql-8.0.15-win64x) in your CLI of choice and run the command `~/mysql-8.0.15-win64x> bin\mysqld --initialize-insecure --console`
    e. run `~/mysql-8.0.15-win64x> bin\mysqld --console` to spin up the server. This should create a mysql server instance running LocalHost:[some port, probably 3306]
    f. Open another console, navigate to the mysql server directory, and run the command `~/mysql-8.0.15-win64x>bin\mysql -u root --skip-password`
    g. Run the command `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '<yourpasswordhere>'`
    h. Leave the server spinning. We're about to use it.
    i. For now, we'll just use the default `mysql` database and dump everything there.
2. Download and install the required packages `~/>python -m pip install requests mysql-connector`:
    a. requests
    b. mysql-connector
3. Open and edit `table_gen.py`.
    a. Fill out the MySQL Connector args in `conn` using the appropriate arguments.
    b. `n` is the number of characters to load. Default 15.
    c. `distinct` is if we want `n` distinct characters.
4. Run the file using your python interpreter (assuming you've installed the requirements, mysql-connector and requests):
    a. `~/>python.exe table_gen.py`
    b. NOTES:
        i. the statements that create `dim_character`, `dim_film`, and `fact_appearance` are all idempotent. This script can be run as many times as you want and there should only be one row per film, character, and film/character combo in each table, respectively.
        ii. `inter_*` tables are not due to assessment constraints (`CREATE` `INSERT` `SELECT`)
    c. run `~/mysql-8.0.15-win64x> bin\mysqldump -u root -p mysql --no-data > ../db.sql` to dump schema information into your folder.
5. After you're satisfied with your tables, export them for later.
6. Run `task_one.py` using your python interpreter (assuming you've installed the requirements, mysql-connector)
    a. `~>python.exe task_one.py`
7. Run `task_two.py` using your python interpreter (assuming you've installed the requirements, requests)