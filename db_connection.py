import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import sql


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

def connection():
    load_dotenv('.env')
    db = 'MyMusicList'
    pw = os.getenv('PASSWORD')
    db_connection = create_db_connection('localhost', 'root', pw, db)

    if not db_connection:
        server_connection = create_server_connection('localhost', 'root', pw)
        sql.create_database(server_connection, sql.create_database)
        db_connection = create_db_connection('localhost', 'root', pw, db)
        sql.execute_query(db_connection, sql.create_planning_table)
        sql.execute_query(db_connection, sql.create_completed_table)
        print('Established connection with MyMusicList database and created necessery tables.')

    return db_connection
