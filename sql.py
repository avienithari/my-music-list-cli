import os
from mysql.connector import Error
import queries


cwd = os.getcwd()

create_database_query = "CREATE DATABASE MyMusicList"

create_planning_table = """
CREATE TABLE Planning (
    id INT,
    band_name VARCHAR(100) NOT NULL PRIMARY KEY
);
"""

create_completed_table = """
CREATE TABLE Completed (
    id INT,
    band_name VARCHAR(100) NOT NULL PRIMARY KEY
);
"""

read_last_element_planning = """
SELECT * from Planning ORDER BY id DESC LIMIT 1;
"""

read_last_element_completed = """
SELECT * from Completed ORDER BY id DESC LIMIT 1;
"""

read_planning = """
SELECT *
FROM Planning ORDER BY band_name ASC;
"""

read_completed = """
SELECT *
FROM Completed ORDER BY band_name ASC;
"""

drop_table_planning = """
DROP TABLE Planning;
"""

drop_table_completed = """
DROP TABLE Completed;
"""

restore_query = f"""
LOAD DATA INFILE '{cwd}/planning_backup.csv'
INTO TABLE Planning
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
"""

index_update = """
CREATE TABLE temporary SELECT * FROM Planning;
TRUNCATE TABLE Planning;
ALTER TABLE Planning AUTO_INCREMENT = 1;
INSERT INTO Planning SELECT band_name FROM temporary ORDER BY id;
DROP TABLE temporary;
"""

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

