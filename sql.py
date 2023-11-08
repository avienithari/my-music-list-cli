import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import queries


load_dotenv('.env')
pw = os.getenv('PASSWORD')
db = 'MyMusicList'

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password)
    except Error as err:
        print(f'Error occured: {err}')

    return connection

def create_database(connection, query): 
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('DB for MyMusicList created succesfully.')
    except Error as err:
        print(f'Error occured: {err}')     

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        print(f'Error: {err}')

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            db = db_name)
    except Error as err:
        pass

    return connection

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f'Error: {err}')
    return result

def fetch_table_data(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f'select * from {table_name}')
    rows = cursor.fetchall()
    return rows

def backup(table_name, file_name):
    with open(file_name, 'w', newline='') as csv_file:
        rows = fetch_table_data(connection, table_name)
        for row in rows:
            csv_file.write(','.join(str(value) for value in row) + '\n')

        print(str(len(rows)) + f' {table_name} elements backuped.')

def restore(table_name, file_name):
    execute_query(connection, queries.restore)

