import sql
import db_connection as db
import pandas as pd
from tabulate import tabulate
import random as rd
import queries

print('Welcome to MyMusicList\nType l for list, r for random, s for search or enter to quit. ')

def search_mode(db_connection):
    band_name = input('Please enter band name: ')
    print(f'Looking for {band_name.title()}')
    planning_table = sql.read_query(db_connection, queries.read_planning)
    completed_table = sql.read_query(db_connection, queries.read_completed)
    planning_counter = 0
    completed_counter = 0

    for value in planning_table:
        if value[1].lower() == band_name.lower():
            planning_counter += 1 
            print(f'{band_name.title()} found in planning.')
            move_band(band_name, value[0], db_connection)
            main()

    for value in completed_table:
        if value[1].lower() == band_name.lower():
            completed_counter += 1 
            print(f'{band_name.title()} found in completed.')
            main()
    
    if planning_counter + completed_counter == 0:
        print(f'{band_name.title()} not listed.')
        decision = input(f'Do you want to add {band_name.title()} to Planning? y/N: ')

        if decision.lower() == 'y':
            query = f"""
            INSERT INTO Planning VALUES
            ({len(planning_table) + 1}, '{band_name.title()}');
            """
            sql.execute_query(db_connection, query)
            print(f'Added {band_name.title()} to Planning.')
            main()
        elif decision.lower() == 'n' or decision.lower() == '':
            main()
        else:
            pass 
        
def random_mode(db_connection):
    planning_indexes = [ values[0] for values in sql.read_query(db_connection, queries.read_planning) ]
    random_band_number = rd.choice(planning_indexes)
    read_element_by_id = f"""
    SELECT * FROM Planning WHERE ID = {random_band_number};
    """
    band_name = sql.read_query(db_connection, read_element_by_id)[0][1]
    print(f'Band for today is: {band_name}')

    rerun = input('Redraw band? y/N: ' )

    if rerun.lower() == 'y':
        random_mode(db_connection)

    elif rerun.lower() == 'n' or rerun.lower() == '':
        move_band(band_name, random_band_number, db_connection)
        main()
        
def list_mode(db_connection):
    planning_results = sql.read_query(db_connection, queries.read_planning)
    completed_results = sql.read_query(db_connection, queries.read_completed)
    planning_table = []
    completed_table = []

    for result in planning_results:
        result = list(result)
        planning_table.append(result)
    
    for result in completed_results:
        result = list(result)
        completed_table.append(result)

    columns = ['id', 'Band Name']
    planning_dataframe = pd.DataFrame(planning_table, columns=columns)
    planning_dataframe = planning_dataframe[planning_dataframe.columns[1:]]
    completed_dataframe = pd.DataFrame(completed_table, columns=columns)
    completed_dataframe = completed_dataframe[completed_dataframe.columns[1:]]
    print('\n       Planning\n', tabulate(planning_dataframe, headers='keys', tablefmt='psql'))
    print('\n       Completed\n', tabulate(completed_dataframe, headers='keys', tablefmt='psql'))

    choice = input('\nExit? y/N: ')
    if choice.lower() == 'n' or choice.lower() == '':
        print('\n')
        main()

    elif choice.lower() == 'y': 
        exit()

    else:
        pass 

def move_band(band_name, band_index, db_connection):
    move_band = input(f'Move {band_name.title()} from Planning to Completed? y/N: ')

    try:
        last = sql.read_query(db_connection, queries.read_last_element_completed)[0][0]
    except IndexError:
        last = 0

    if move_band.lower() == 'y':
        add_band_to_completed = f"""
        INSERT INTO Completed VALUES
        ({last + 1}, '{band_name.title()}');
        """
        sql.execute_query(db_connection, add_band_to_completed) 
        delete_moved_band_from_planning = f"""
        DELETE FROM Planning WHERE id = {band_index};
        """
        sql.execute_query(db_connection, delete_moved_band_from_planning)
        print(f'Moved {band_name.title()} from Planning to Completed.') 

def root(db_connection):
    command = input('\nroot> ')

    if command.lower() == 'populate': 
        sql.execute_query(db_connection, queries.populate)
        print('Populated tables')
        root(db_connection)

    elif command.lower() == 'delete':
        table = input('From which table?: ')
        delete_band = input('Which band?: ')
        delete = f"""
        DELETE FROM {table.title()} WHERE band_name='{delete_band.title()}';
        """
        sql.execute_query(db_connection, delete)
        print(f'Deleted {delete_band.title()} from {table.title()}.')
        root(db_connection)

    elif command.lower() == 'drop':
        warning = input('Are you sure you want to proceed? y/N:')

        if warning.lower() == 'y':
            sql.execute_query(db_connection, queries.drop_table_completed)
            sql.execute_query(db_connection, queries.drop_table_planning)
            print('Dropped tables.')
            print('NOTE: You ought to create tables via setup command after dropping so program can work properly.')

        root(db_connection)

    elif command.lower() == 'setup':
        sql.execute_query(db_connection, queries.create_planning_table)
        sql.execute_query(db_connection, queries.create_completed_table)
        print('Created Planning and Completed tables.')
        root(db_connection)

    elif command.lower() == 'backup':
        sql.backup(table_name='Planning', file_name='planning_backup.csv')
        sql.backup(table_name='Completed', file_name='completed_backup.csv')
        root(db_connection)

    elif command.lower() == 'restore':
        sql.restore(table_name='Planning', file_name='planning_backup.csv')
        # sql.restore(table_name='Completed', file_name='completed_backup.csv')
        pass

    elif command.lower() == '':
        main()
        
def main():
    db_connection = db.connection()
    
    mode = input('\nMode: ')

    if mode.lower() == 's':
        search_mode(db_connection)

    elif mode.lower() == 'r':
        random_mode(db_connection)

    elif mode.lower() == 'l':
        list_mode(db_connection)
        
    elif mode.lower() == 'root':
        print('\nAvailable commands:\n\
        delete (band)\n\
        drop (tables)\n\
        setup (tables)\n\
        backup\n\
        restore\n\nPress enter to exit root.')
        root(db_connection)

    elif mode.lower() == '':
        exit()

if __name__ == "__main__":
    main()
