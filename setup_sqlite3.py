'''Make SQLite3 available to the project'''

import os
from sqlite_commands import create_db

# Check if there is a SQLite folder
if not os.path.isdir('./sqlite'):
    print('Installing SQLite3')
    os.system(
        'git clone https://github.com/guilherme-daros/sqlite3-setup.git sqlite')
    os.chdir('sqlite')
    # Check if there is a db folder inside SQLite folder
    if not os.path.isdir('./db'):
        os.system('mkdir db')
        os.chdir('../')
else:
    print('SQLite is already installed')

# Checks is main database exists
if not os.listdir('./sqlite/db/'):
    print('Creating Main database')
    create_db(input('Main DB name: '))
else:
    print('Main database already exists')
