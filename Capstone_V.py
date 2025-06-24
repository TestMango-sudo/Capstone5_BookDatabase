# Task 48 - Capstone V

#==========Import Section===============
import sqlite3
from tabulate import tabulate

#=========Pre-declard Variables etc=====
BLUE = '\033[94m'
YELLOW = '\033[93m'
LIGHTRED = '\033[91m'


# Creation of Database
db = sqlite3.connect('ebookstore')

# create table
book_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
    (3006, "The Tombs of Atuan", "Ursula Le Guin", 21),
    (3007, "The Dragon's of Autumn Twilight", "Margaret Weis and Tracy Hickman", 51),
    (3008, "Altered Carbon", "Richard Morgan", 8),
    (3009, "The Black Company", "Glen Cook", 65),
    (3010, "Javascript and JQuery", "Jon Duckett", 17),
    (3011, "Pages of Pain", "Troy Denning", 42),
    (3012, "Brisingr", "Christopher Paolini", 11),
    (3013, "Hollow City", "Ransom Riggs", 24),
    (3014, "The Ragged Trousered Philantropists", "Robert Trussell", 34),
    (3015, "Das Kapital", "Karl Marx", 5)]

cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, 
            author TEXT, stock INTEGER) ''')
db.commit()
cursor.executemany('''INSERT OR REPLACE INTO books (id, title, author, stock)
                     VALUES(?,?,?,?) ''',(book_list))
db.commit()


def table_view(data):
    #Tabulation of Data for displaying booklist
	heading = ["ID", "Title", "Author", "Quantity"]

	print(tabulate(data, heading, tablefmt="rounded_grid"))


def view_all_books():
    data=cursor.execute('''SELECT * FROM books ''').fetchall()
    table_view(data)


def enter_book():
    # Get the Last Highest ID from database and automatically add one. This will be the new id.
    last_id = cursor.execute('''SELECT MAX(id) FROM books''').fetchone()
    new_id = last_id[0]+1
    new_id = int(new_id)
    
    # Get rest of book details.
    b_title = input("Please enter the title of the book: ")
    b_auth = input("Please enter the author: ")
    b_stock = int(input("Please enter the amount of copies available in stock: "))
    print("Adding book to system......")

    # add book to database:
    cursor.execute('''INSERT INTO books (id, title, author, stock)
                     VALUES(?,?,?,?) ''',(new_id, b_title, b_auth, b_stock))
    db.commit()
    last_book_added = cursor.execute(''' SELECT * FROM books where title = ? ''',(b_title,)).fetchall()
    for row in last_book_added:
        print(f'''
            =======New Book Added============
            Database ID: {row[0]}
            Title: {row[1]}
            Author: {row[2]}
            Quantity in Stock: {row[3]}
            =================================
            ''')

def delete_book():
    # Code for Deleting selected book from database.
    rem_book = int(input("Please enter the ID of the book you wish to remove: "))
    data = cursor.execute('''SELECT * FROM books WHERE id = ? ''', (rem_book,))
    if not data:
        print("No books found matching those criteria. Please try again.")
        return
    else:
        cursor.execute('''DELETE FROM books WHERE id = ? ''',(rem_book,))
        db.commit()
        print(f"Any Books in database with the title {rem_book} have been removed")
        return


def update_book():
    # Code for allowing user to update a book on the database.
    up_id = int(input("Please enter the ID of the book you wish to update: "))
    cursor.execute
    update_book = cursor.execute(''' SELECT * FROM books where id = ? ''',(up_id,)).fetchall()

    # handle if not found
    if not update_book:
        print("No items found matching those criteria. Please try again.")
        return
    else:
        for row in update_book:
            print(f'''
                =======Book Selected============
                ID: {row[0]}
                Title: {row[1]}
                Author: {row[2]}
                Quantity in stock: {row[3]}
                =================================
                ''')
        while True:
            output=(f"{BLUE}|————————————————————————————————————————————|\n")
            output += (f"|{YELLOW}    e-Book Manager Version 1.2  {BLUE}            |\n")
            output += (f"|{YELLOW}    What would you like to edit?{BLUE}            |\n")
            output += (f"{BLUE}|                                            |\n")
            output += (f"| {LIGHTRED}           Edit Menu   {BLUE}                    |\n")
            output += (f"|{YELLOW}          1. Edit Title                     {BLUE}|\n")
            output += (f"|{YELLOW}          2. Edit Author                    {BLUE}|\n")
            output += (f"|{YELLOW}          3. Edit Stock Quantity            {BLUE}|\n")
            output += (f"|{YELLOW}          4. Main Menu             {BLUE}         |\n")
            output += (f"{BLUE}|                                            |\n")
            output += (f"{BLUE}|————————————————————————————————————————————|\n")
            print(output)
            choice = int(input(f"{YELLOW}Enter Choice:"))
            
            if choice == 1:
                print("Please enter a new title: ")
                new_title = input("")
                repl_title = update_book[0][1]
                cursor.execute('''UPDATE books SET title = ? WHERE title = ?''', (new_title, repl_title,))
                db.commit()
                print("Database updated.")
                update_book = cursor.execute(''' SELECT * FROM books where title = ? ''',(new_title,)).fetchall()
                for row in update_book:
                    print(f'''
                        =========Amended Book============
                        ID: {row[0]}
                        Title: {row[1]}
                        Author: {row[2]}
                        Quantity in stock: {row[3]}
                        =================================
                        ''')
                return      

            elif choice == 2:
                # Code for amendeding by Author.
                print("Please enter a new Author: ")
                new_auth = input("")
                repl_auth = update_book[0][2]
                cursor.execute('''UPDATE books SET author = ? WHERE title = ? AND author = ?''', 
                                    (new_auth, update_book[0][1], repl_auth,))
                db.commit()
                print("Database updated.")
                update_book = cursor.execute(''' SELECT * FROM books where author = ? ''',(new_auth,)).fetchall()
                for row in update_book:
                    print(f'''
                        =========Amended Book============
                        ID: {row[0]}
                        Title: {row[1]}
                        Author: {row[2]}
                        Quantity in stock: {row[3]}
                        =================================
                        ''')
                return
                
            elif choice == 3:
                    # Code for amendeding stock.
                print("Please enter a new stock amount: ")
                new_stock = int(input(""))
                repl_stock = update_book[0][3]
                cursor.execute('''UPDATE books SET stock = ? WHERE title = ? AND stock = ?''', 
                            (new_stock, update_book[0][1], repl_stock,))
                db.commit()
                print("Database updated.")
                update_book = cursor.execute(''' SELECT * FROM books where title = ? ''',(update_book[0][1],)).fetchall()
                for row in update_book:
                    print(f'''
                        =========Amended Book============
                        ID: {row[0]}
                        Title: {row[1]}
                        Author: {row[2]}
                        Quantity in stock: {row[3]}
                        =================================
                        ''')
                return
            
            else:
                print("Your choice has not been recognised, Please Try again")

def search_book():
    # Code allowing user to search via title, author or ID.
    while True:
                output=(f"{BLUE}|————————————————————————————————————————————|\n")
                output += (f"|{YELLOW}    e-Book Manager Version 1.2  {BLUE}            |\n")
                output += (f"|{YELLOW}  How would you like to search?{BLUE}             |\n")
                output += (f"{BLUE}|                                            |\n")
                output += (f"| {LIGHTRED}           Edit Menu   {BLUE}                    |\n")
                output += (f"|{YELLOW}     1. Search by Title                     {BLUE}|\n")
                output += (f"|{YELLOW}     2. Searh by Author                     {BLUE}|\n")
                output += (f"|{YELLOW}     3. Search ID                           {BLUE}|\n")
                output += (f"|{YELLOW}     4. Main Menu                  {BLUE}         |\n")
                output += (f"{BLUE}|                                            |\n")
                output += (f"{BLUE}|————————————————————————————————————————————|\n")
                print(output)
                choice = int(input(f"{YELLOW}Enter Choice:"))
                
                if choice == 1:
                    # search by Title.
                    search_title = input("Please enter a title to search: ")
                    search_results = cursor.execute('''SELECT * FROM books WHERE title = ?''', (search_title,)).fetchall()
                    if not search_results:
                        print("No items found matching those criteria. Please try again.")
                        return
                    else:
                        for row in search_results:
                            print(f'''
                                =========Search Results==========
                                ID: {row[0]}
                                Title: {row[1]}
                                Author: {row[2]}
                                Quantity in stock: {row[3]}
                                =================================
                                ''')
                        return      

                elif choice == 2:
                    # Code for searching by author.
                    search_auth = input("Please enter an author to search: ")
                    search_results = cursor.execute('''SELECT * FROM books WHERE author = ?''', (search_auth,)).fetchall()
                    if not search_results:
                        print("No items found matching those criteria. Please try again.")
                        return
                    else:
                        for row in search_results:
                            print(f'''
                                =========Search Results==========
                                ID: {row[0]}
                                Title: {row[1]}
                                Author: {row[2]}
                                Quantity in stock: {row[3]}
                                =================================
                                ''')
                        return      
                    
                elif choice == 3:
                    # Search by ID
                    search_id = int(input("Please enter an ID number to search: "))
                    search_results = cursor.execute('''SELECT * FROM books WHERE id = ?''', (search_id,)).fetchall()
                    if not search_results:
                        print("No items found matching those criteria. Please try again.")
                        return
                    else:
                        for row in search_results:
                            print(f'''
                                =========Search Results==========
                                ID: {row[0]}
                                Title: {row[1]}
                                Author: {row[2]}
                                Quantity in stock: {row[3]}
                                =================================
                                ''')
                        return

                elif choice == 4:
                    main_menu()    
                    
                else:
                    print("Your choice has not been recognised, Please Try again")


#==========Main Menu=============

def main_menu():

    while True:
        try:
            output=(f"{BLUE}|————————————————————————————————————————————|\n")
            output += (f"|{YELLOW}    Welcome to e-Book Manager Version 1.2  {BLUE} |\n")
            output += (f"|{YELLOW} Select one of the following Options below:{BLUE} |\n")
            output += (f"{BLUE}|                                            |\n")
            output += (f"| {LIGHTRED}          MAIN MENU    {BLUE}                    |\n")
            output += (f"|{YELLOW}          1. Enter book.                   {BLUE} |\n")
            output += (f"|{YELLOW}          2. Update book                   {BLUE} |\n")
            output += (f"|{YELLOW}          3. Delete book                   {BLUE} |\n")
            output += (f"|{YELLOW}          4. Search books                  {BLUE} |\n")
            output += (f"|{YELLOW}          5. View all books                {BLUE} |\n")
            output += (f"|{YELLOW}          0. Exit Program                  {BLUE} |\n")
            output += (f"{BLUE}|                                            |\n")
            output += (f"{BLUE}|————————————————————————————————————————————|\n")
            print(output)
            choice = int(input(f"{YELLOW}Enter Choice:"))
            if choice == 1:
                enter_book()
                while True:
                    output=(f"{BLUE}|————————————————————————————————————————————|\n")
                    output += (f"|{YELLOW}    e-Book Manager Version 1.2  {BLUE}            |\n")
                    output += (f"|{YELLOW} Select one of the following Options:{BLUE}       |\n")
                    output += (f"{BLUE}|                                            |\n")
                    output += (f"| {LIGHTRED}         Delete Menu   {BLUE}                    |\n")
                    output += (f"|{YELLOW}          1. Enter another book             {BLUE}|\n")
                    output += (f"|{YELLOW}          2. back to Main Menu              {BLUE}|\n")
                    output += (f"{BLUE}|                                            |\n")
                    output += (f"{BLUE}|————————————————————————————————————————————|\n")
                    print(output)
                    choice = int(input(f"{YELLOW}Enter Choice:"))
                    if choice == 1:
                        enter_book()

                    elif choice == 2:
                        main_menu()
                    else:
                        print("Your choice has not been recognised, Please Try again")


            elif choice == 2:
                update_book()
                while True:
                    try:
                        output=(f"{BLUE}|————————————————————————————————————————————|\n")
                        output += (f"|{YELLOW}    e-Book Manager Version 1.2  {BLUE}            |\n")
                        output += (f"|{YELLOW} Select one of the following Options:{BLUE}       |\n")
                        output += (f"{BLUE}|                                            |\n")
                        output += (f"| {LIGHTRED}         Delete Menu   {BLUE}                    |\n")
                        output += (f"|{YELLOW}          1. Update another book            {BLUE}|\n")
                        output += (f"|{YELLOW}          2. back to Main Menu              {BLUE}|\n")
                        output += (f"{BLUE}|                                            |\n")
                        output += (f"{BLUE}|————————————————————————————————————————————|\n")
                        print(output)
                        choice = int(input(f"{YELLOW}Enter Choice:"))
                        if choice == 1:
                            update_book()

                        elif choice == 2:
                            main_menu()
                    except ValueError:
                        print("Your choice has not been recognised, Please Try again")

            elif choice == 3:
                delete_book()
                while True:
                    try:
                        output=(f"{BLUE}|————————————————————————————————————————————|\n")
                        output += (f"|{YELLOW}    e-Book Manager Version 1.2  {BLUE}            |\n")
                        output += (f"|{YELLOW} Select one of the following Options:{BLUE}       |\n")
                        output += (f"{BLUE}|                                            |\n")
                        output += (f"| {LIGHTRED}         Delete Menu   {BLUE}                    |\n")
                        output += (f"|{YELLOW}          1. Delete another book            {BLUE}|\n")
                        output += (f"|{YELLOW}          2. back to Main Menu              {BLUE}|\n")
                        output += (f"{BLUE}|                                            |\n")
                        output += (f"{BLUE}|————————————————————————————————————————————|\n")
                        print(output)
                        choice = int(input(f"{YELLOW}Enter Choice:"))
                        if choice == 1:
                            delete_book()

                        elif choice == 2:
                            main_menu()
                    except ValueError:
                        print("Your choice has not been recognised, Please Try again")
                    
            elif choice == 4:
                search_book()
                while True:
                    try:
                        output=(f"{BLUE}|————————————————————————————————————————————|\n")
                        output += (f"|{YELLOW}    e-Book Manager Version 1.2  {BLUE}            |\n")
                        output += (f"|{YELLOW} Select one of the following Options:{BLUE}       |\n")
                        output += (f"{BLUE}|                                            |\n")
                        output += (f"| {LIGHTRED}         Delete Menu   {BLUE}                    |\n")
                        output += (f"|{YELLOW}          1. Search for another book        {BLUE}|\n")
                        output += (f"|{YELLOW}          2. back to Main Menu              {BLUE}|\n")
                        output += (f"{BLUE}|                                            |\n")
                        output += (f"{BLUE}|————————————————————————————————————————————|\n")
                        print(output)
                        choice = int(input(f"{YELLOW}Enter Choice:"))
                        if choice == 1:
                            search_book()

                        elif choice == 2:
                            main_menu()
                    except ValueError:
                        print("Your choice has not been recognised, Please Try again")


            elif choice == 5:
                view_all_books()


            elif choice == 0:
                # code to exit program
                print("Closing Database Connections...")
                db.close()
                print('Goodbye!!!')
                exit()
            
        except ValueError:
                print("Your choice has not been recognised, Please Try again")
main_menu()