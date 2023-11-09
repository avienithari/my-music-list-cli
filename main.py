import source
import db_connection as db


print('Welcome to MyMusicList\nType l for list, r for random, s for search or enter to quit. ')
        
def main():
    db_connection = db.connection()
    
    mode = input('\nMode: ')

    if mode.lower() == 's':
        source.search_mode(db_connection)

    elif mode.lower() == 'r':
        source.random_mode(db_connection)

    elif mode.lower() == 'l':
        source.list_mode(db_connection)
        
    elif mode.lower() == 'root':
        print('\nAvailable commands:\n\
        delete (band)\n\
        drop (tables)\n\
        setup (tables)\n\
        backup\n\
        restore\n\nPress enter to exit root.')
        source.root(db_connection)

    elif mode.lower() == '':
        exit()

    main()

if __name__ == "__main__":
    main()
