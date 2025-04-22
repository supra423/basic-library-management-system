# this started out as an object-oriented programming project 
# until I kept on updating and updating the source 
# and now it is heavily reliant on SQLite databases
# still has a bit of OOP in it tho
# Alexus Roa BSIT-1R1
import sqlite3

class Library(): 
    '''
    a class to store, delete, and display books
    '''
    def __init__(self):

        # defining conventional sql variables that will come in handy
        self.connection = sqlite3.connect('bookshelf.s3db')
        self.cursor = self.connection.cursor()
        
        # create a table inside the bookshelf file named 'books'
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS books
            (
                Number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                  
                Title TEXT NOT NULL,
                Author TEXT NOT NULL,
                Book_ID TEXT NOT NULL,
                Available_Copies INTEGER NOT NULL DEFAULT 1                
            );
                             
            CREATE TABLE IF NOT EXISTS borrow_history
            (
                Number INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                  
                User TEXT NOT NULL,
                Title TEXT NOT NULL,
                Author TEXT NOT NULL,
                Book_ID TEXT NOT NULL,
                Borrow_date TEXT NOT NULL,
                Return_date TEXT NULL
            );                              
                            ''')
        self.connection.commit()
        
    def add_book(self): 
        '''
        add book function, basically selects the 'Book_ID' column from the 'books' table,
        fetches all ID Numbers from that column, adds a new row in the table if the ID number 
        that was inputted does not exist yet in the table.
        ''' 
        c = self.connection.cursor() 
        # list comprehension instead of using row factory, stack overflow be giving bad advices lol
        stored_idNos = [row[0] for row in c.execute("select Book_ID from books").fetchall()]

        while True: # loop breaks when a book is successfully added

            try:
                title = input("Enter book title:\n").strip()
                author = input("Enter author:\n").strip()
                idNo = input("Enter ID Number:\n").strip()
                amount_of_books = int(input("Enter amount of books:\n").strip())
            except Exception:
                print("Error! Please try again!")
                break

            if amount_of_books > 0: 
            # checks first if amount of books inputted by the user is less than 0 before checking if ID number is in database
                if idNo not in stored_idNos:

                    try:
                        c.execute("insert into books(Title, Author, Book_ID, Available_Copies) values (?, ?, ?, ?) ", (title, author, idNo, amount_of_books))
                        self.connection.commit()
                        print(f'Book "{title}" added successfully!\n')
                        break

                    except Exception:
                        print("Error! Please try again!")

                else: # since the ID number of a book is its unique identifier
                    # this program automatically assumes two books are the same
                    # even if both books' title and author are different,
                    # as long as they both share the same ID Numbers.
                    c.execute("update books set Available_Copies = Available_Copies + (?) where Book_ID = ?", (amount_of_books, idNo))
                    self.connection.commit()
                    print(f'Book "{title}" added successfully!\n')
                    break
            else:
                print("Amount of book(s) must be at least 1!")

    def remove_book(self): 
        ' deletes all copies of a book from the database by specifying its ID number '
        
        idNo = input("Enter ID Number:\n").strip()

        c = self.connection.cursor()
        stored_idNos = c.execute("select Book_ID from books where Book_ID = ?", (idNo,)).fetchone()

        if stored_idNos:
            c.execute("delete from books WHERE Book_ID = ?", (idNo,))
            self.connection.commit()

            print(f'Book has been removed successfully!')
        else:
            print("That book doesn't exist in this library!\n")

    def display_books(self): 
        '''
        select all from books and then fetch everything
        each fetched 'book' is then stored inside a tuple, lets say: 
        ('Python Basics', 'Alexus Roa', '1234567890')
        and then each tuple is automatically stored inside a list:

        [('Python Basics', 'Alexus Roa', '1234567890'), 
        ('SQLITE DATABASES', 'Alexus Roa', '0987654321')]
        '''

        books = self.cursor.execute('SELECT * FROM books').fetchall()        

        if not books:
            print("\nNo books are available!\n")
            return

        print("\nThese are the books currently in the library:\n")
        for book in books:
            print(f'Title: {book[1]} \nAuthor: {book[2]} \nID Number: {book[3]} \nAvailable copies: {book[4]}\n')
            # since 'book' is a tuple, those numbers (0, 1, 2, 3) are indexes of the tuple

    def search_book(self):
        '''
        This function fetches a row from the books table and then searches for a book that matches
        the ID number that was inputted by the user and then displays that particular book
        '''
        idNo = input("Enter ID Number:\n").strip()
        c = self.connection.cursor()
        book_find = c.execute("SELECT Title, Author, Book_ID, Available_Copies from books where Book_ID = ?", (idNo,)).fetchone()
        
        if book_find:
            print(f'\nTitle: {book_find[0]} \nAuthor: {book_find[1]} \nID Number: {book_find[2]} \nAvailable copies: {book_find[3]}\n')
        else:
            print("\nThat book doesn't exist!")
