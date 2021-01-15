'''Defines a Class to SQLite Databases'''

import os
import sqlite3

from sqlite3 import Error
from time import localtime, sleep
from random import randint


class WateringSysDB:
    '''Instantiates a SQLite3 Database'''

    def __init__(self, name):
        '''Initiates a instace of SQLiteDB

        Args:
            name (str): name of database to be created
        '''
        if not os.path.isdir('./sqlite'):
            os.system(
                'git clone https://github.com/guilherme-daros/sqlite3-setup.git sqlite')
            os.chdir('sqlite')
            # Check if there is a db folder inside SQLite folder
            if not os.path.isdir('./db'):
                os.system('mkdir db')
                os.chdir('../')
        self.name = name
        self.path = rf'sqlite\db\{self.name}.db'

        try:
            connector = sqlite3.connect(self.path)
        except Error as error:
            print(error)
        finally:
            if connector:
                connector.close()

    def create_table(self, table_name, columns):
        '''Create a table on the database

        Args:
            table_name (str): name of table to be created
            columns (list): name od columsn to be created on table
        '''
        try:
            connector = sqlite3.connect(self.path)
            cursor = connector.cursor()

            command = f'CREATE TABLE {table_name} (date, time,'
            for column in columns[:-1]:
                command += column+','
            command += columns[-1]+');'

            cursor.execute(command)

        except Error as error:
            print(error)

        finally:
            if connector:
                connector.close()

    def get_tables(self):
        '''
        Returns:
            list: a list with the tables inside the database
        '''
        try:
            connector = sqlite3.connect(self.path)
            cursor = connector.cursor()
            cursor.execute(
                'SELECT name FROM sqlite_master WHERE type="table";')
            query = cursor.fetchall()
            ret = []

            for data in query:
                ret.append(data[0])
            return ret

        except Error as error:
            print(error)

    def insert_data(self, table_name, **kwargs):
        '''Insert data in a selected table into the database

        Args:
            table_name (str): table to insert data into
            kwargs (dict): key:value pair of name:data to be inserted
        '''

        try:
            connector = sqlite3.connect(self.path)
            cursor = connector.cursor()

            date = f'{localtime().tm_mday}/{localtime().tm_mon}/{localtime().tm_year}'
            time = f'{localtime().tm_hour}:{localtime().tm_min}:{localtime().tm_sec}'

            values = [date, time]
            keys = list(kwargs.keys())

            for value in kwargs.values():
                values.append(value)

            command = f'INSERT INTO {table_name} (date, time,'

            for key in keys[:-1]:
                command += key+','
            command += f'{keys[-1]}) VALUES (?,?,'

            for _ in keys[:-1]:
                command += '?,'
            command += '?)'

            print(command)
            cursor.execute(command, values)
            connector.commit()

        except Error as error:
            print(error)
        finally:
            connector.close()

    def get_moisture_data(self, node_id, day):
        '''Gets moisture data from a specific node at a specific day

        Args:
            node_id (int): node_id to get data
            day (str): DD/MM/YYYY formated day string to get data

        Returns:
            list: list of tuples with (date, moisture) format
        '''

        try:
            connector = sqlite3.connect(self.path)
            cursor = connector.cursor()
            command = f'SELECT time, moisture FROM nodes_moisture_data WHERE  node_id={node_id} AND date="{day}";'
            cursor.execute(command)
            query = cursor.fetchall()
            return query
        except Error as error:
            print(error)

    def execute_script(self, script_path):
        '''Executes a .sql scrip in the database instance

        Args:
            script_path (str): path to the .sql script
        '''

        try:
            connector = sqlite3.connect(self.path)
            cursor = connector.cursor()
            cursor.executescript(open(script_path).read())

        except Error as error:
            print(error)
        finally:
            connector.close()


db = WateringSysDB('database')

# db.execute_script('setup.sql')
# i = 0
# while i < 100:
#     db.insert_data('nodes_moisture_data', node_id=randint(
#         1, 10), moisture=randint(1, 100))
#     sleep(1)
#     i += 1

print(db.get_moisture_data('8', '14/1/2021'))

