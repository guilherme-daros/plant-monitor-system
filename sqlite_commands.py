'''
Defines useful commands for dealing with SQLite Databases
'''
import sqlite3

from sqlite3 import Error


def create_db(db_name):
    '''Create a SQLite database

    Args:
        db_name (str): name of the database to be created

    Returns:
        boolean: true if success
    '''
    connector = None
    db_path = rf'sqlite\db\{db_name}.db'
    try:
        connector = sqlite3.connect(db_path)
        return True
    except Error as error:
        print(error)
    finally:
        if connector:
            connector.close()


def connect_db(db_name):
    '''Connect to a SQLite database

    Args:
        db_name (str): path to .db file

    Returns:
        object: Connection object
    '''
    db_path = rf'sqlite\db\{db_name}.db'
    connector = None
    try:
        connector = sqlite3.connect(db_path)
        return connector
    except Error as error:
        print(error)

    return connector


def create_table(db_name, table_name, *args):
    '''Create a Table on a SQLite database 

    Args:
        db_name (str): database to create table in
        table_name (str): name of the table to be created
        *args (str): name + type of columns to be created on the table

    Returns:
        boolen: true for success
    '''
    try:
        connector = connect_db(db_name)
        cursor = connector.cursor()

        command = f'CREATE TABLE {table_name} ('
        for arg in args[:-1]:
            command += f'{arg},'
        command += f'{args[-1]})'
        cursor.execute(command)
        return True

    except Error as error:
        print(error)


def insert_data(db_name, table_name, *args):
    '''Insert data into a SQLite database table

    Args:
        db_name (str): database where table_name is
        table_name (str): table to insert data in
        *args (str): data to be inserted

    Returns:
        boolean: true for success
    '''
    try:
        connector = connect_db(db_name)
        cursor = connector.cursor()

        cursor.execute(f'SELECT * from {table_name}')
        column_names = [name[0] for name in cursor.description]

        command = f'INSERT INTO {table_name} ('

        for name in column_names[:-1]:
            command += f'{name},'
        command += f'{column_names[-1]}) VALUES ('

        #pylint: disable=unused-variable
        for i in range(len(column_names) - 1):
            command += '?,'
        command += '?)'

        cursor.execute(command, args)
        connector.commit()
        return True
    except Error as error:
        print(error)


def get_data(db_name, table_name, column_name):
    '''Gets data from a specified column table

    Args:
        db_name (str): database where table_name is
        table_name (str): table where column_name is
        column_name (str): column to get data

    Returns:
        list: list with selected data
    '''
    try:
        connector = connect_db(db_name)
        cursor = connector.cursor()
        cursor.execute(f'SELECT {column_name} from {table_name}')
        data = cursor.fetchall()
        ret = []
        i = 0
        for d in data:
            ret.append(d[0])
            i += 1
        return ret
    except Error as error:
        print(error)
