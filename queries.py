import os


cwd = os.getcwd()

create_database = "CREATE DATABASE MyMusicList"

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

populate = f"""
LOAD DATA INFILE '{cwd}/mymusiclist.csv'
INTO TABLE Planning
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
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

delete_query_planning = """
DELETE FROM Planning WHERE id = 4;
"""

delete_query_completed = """
DELETE FROM Completed WHERE id = 3;
"""

drop_table_planning = """
DROP TABLE Planning;
"""

drop_table_completed = """
DROP TABLE Completed;
"""

restore = f"""
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
