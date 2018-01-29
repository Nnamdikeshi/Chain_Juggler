''' Import sqlite'''
import sqlite3

'''Declare our global variables'''
 
global update_id
global chainsawDb
global count
global cur

def db_setup():

    '''Call our global variables, connect to our database, create our table in db'''	

    global chainsawDb
    global cur
    global count

    chainsawDb = sqlite3.connect('chainsaw_juggling_record.db')
    cur = chainsawDb.cursor()
    cur.execute('create table if not exists records (id, name text, country text, catches int)')
    count = count()

    return count

def menu():

    '''Display choices for user, return user choice'''

    print('''
        1. Add Record
        2. View Records
        3. Search and Update
        4. Delete Record
        q. Quit
    ''')

    choice = input('Enter your choice: Ex. "1"')

    return choice

def handle_choice(choice):

    '''Handle user choice'''

    if choice == '1':
        add_jugg(True)

    elif choice == '2':
        print_records(db_return_data())

    elif choice == '3':
        search_jugg()

    elif choice == '4':
        delete_jugg()

    elif choice == 'q':
        db_close()

    else:
        print("Please enter a valid choice")

def db_return_data():

    ''' Returns juggler data with select query '''
	
    global chainsawDb
    global cur

    r = cur.execute('select * from records').fetchall()

    return r

def count():

    global count

    count = len(db_return_data())

    return count


def add_jugg(bool):

    ''' Gather input for juggler '''
	
    name = input("Enter the Jugglers name: ")
    country = input("Enter the Jugglers country of origin: ")
    catches = int(input("Enter the Jugglers # of catches: "))
	# Insert if new data, Update non-new data
    if bool == True:
        db_jugg_insert(name,country,catches)

    elif bool == False:
        db_update_data(name,country,catches)

def print_records(records):

    ''' Print records '''
	
    for record in records:
        print(record)

def update_jugg():

    ''' Gathers user input '''
	
    global count
    global update_id

    update_id = int(input("Enter the id number of the record to update: "))

    if update_id > 0 and update_id <= count:
        add_jugg(False)

def db_update_data(name,country,catches):

    ''' Use update_jugg data to update record in db with update query '''
	
    global chainsawDb
    global cur
    global update_id

    cur.execute('update records set name = ?, country = ?, catches = ? where id = ?', (name, country, catches, update_id))
    chainsawDb.commit()
	
def db_jugg_insert(name, country, catches):
    ''' Insert our data from add_jugg using insert query '''

    global chainsawDb
    global cur
    global count
	# Update counter
    count +=1
    id = count

    cur.execute('insert into records values (?, ?, ?, ?)', (id, name, country, catches))
    chainsawDb.commit()


def search_jugg():

    ''' Gathers user input to find juggler '''

    find = input("Enter a search term: ")

    records = db_return_query_data(find)
	# If input is already in db then update_jugg()
    if len(records) > 0:
        print_records(records)
        update_jugg()

def delete_jugg():

    ''' Gather user input on which juggler to delete '''

    global count

    delete_id = int(input("Enter the id number of the record to delete: "))
    db_delete_data(delete_id)

def db_delete_data(delete_id):

    ''' Uses DELETE query to delete db juggler data '''

    global chainsawDb
    global cur

    cur.execute('DELETE FROM records WHERE id = ?', (delete_id,))
    chainsawDb.commit()

def db_return_query_data(find):

    ''' Uses select query to find our juggler data '''
	
    global chainsawDb
    global cur

    s = cur.execute("select * from records where name like ? or country like ? or catches like ?", (find, find, find)).fetchall()

    return s

def db_close():

    ''' Closes db '''
	
    global chainsawDb

    chainsawDb.commit()
    chainsawDb.close()

    print('Database has been Closed')


def main():
    ''' Main function, run setup, quit if q'''
    db_setup()

    quit = 'q'
    choice = None

    while choice != quit:
        choice = menu()
        handle_choice(choice)

main()