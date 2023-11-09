import os
from dotenv import load_dotenv
import sql
import queries


def connection():
    load_dotenv('.env')
    db = 'MyMusicList'
    pw = os.getenv('PASSWORD')
    db_connection = sql.create_db_connection('localhost', 'root', pw, db)

    if not db_connection:
        server_connection = sql.create_server_connection('localhost', 'root', pw)
        sql.create_database(server_connection, queries.create_database)
        db_connection = sql.create_db_connection('localhost', 'root', pw, db)
        sql.execute_query(db_connection, queries.create_planning_table)
        sql.execute_query(db_connection, queries.create_completed_table)
        print('Established connection with MyMusicList database and created necessery tables.')

    return db_connection
