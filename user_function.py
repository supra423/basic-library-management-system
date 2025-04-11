import sqlite3
import datetime

class User():
    
    def __init__(self, name):
        self.name = name    
        self.connection = sqlite3.connect('bookshelf.s3db')

    def borrow_book(self):
        '''
            Asks for ID number of the book and then fetches a row that matches the ID number specified by the user.
            This function then adds a row to the borrow_history table that records that particular borrow transaction
            and then updates the available copies in the books table by minusing the available copies by one
        '''
        idNo_borrow = input("Please enter the ID Number of the book you want to borrow:\n").strip()

        c = self.connection.cursor() 
        available_books = c.execute("select Title, Author, Book_ID, Available_Copies from books WHERE Book_ID = ?", (idNo_borrow,)).fetchone()

        if available_books and available_books[3] > 0:

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            empty_timestamp = ''            
            # sorry for the REAAAALLLLYYYYY LONG line
            c.execute("insert into borrow_history(User, Title, Author, Book_ID, Borrow_date, Return_date) values (?, ?, ?, ?, ?, ?)", (self.name, available_books[0], available_books[1], available_books[2], timestamp, empty_timestamp))
            c.execute("update books set Available_Copies = Available_Copies - 1 WHERE Book_ID = ?", (available_books[2],))
            self.connection.commit()
            print(f'{self.name} borrowed "{available_books[0]}"')
        else:
            print("A book with that ID does not exist or is out of copies in the library!")

    def return_book(self):
        '''
        What this function does is that it first fetches a row from the borrow_history table where it matches the
        name of the user returning the book and the book id, and when the return date
        '''
        idNo_return = input("Please enter the ID Number of the book you want to return:\n").strip()
        empty_string = ''
        c = self.connection.cursor()
        borrowed_books = c.execute("select Number, User, Title, Book_ID, Return_date from borrow_history WHERE User = ? and Book_ID = ? and Return_date = ?", (self.name, idNo_return, empty_string)).fetchone()

        try:
        #for borrowed_book in borrowed_books:
            if self.name in borrowed_books and idNo_return in borrowed_books and borrowed_books[4] == '':
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("update books set Available_Copies = Available_Copies + 1 WHERE Book_ID = ?", (idNo_return,))
                c.execute("update borrow_history set Return_date = (?) WHERE Number = ? AND Book_ID = ? AND User = ?", (timestamp, borrowed_books[0], idNo_return, self.name))
                self.connection.commit()
                print(f'{self.name} returned "{borrowed_books[2]}"')
                    
            else:
                    print("Book is not successfully returned")

        except Exception:
            print("Error! Please try again!")
            
    def display_borrowed_books(self):
        '''
        A function that fetches all the books from the borrow_history table that corresponds to the
        user that made the request.
        '''
        c = self.connection.cursor()

        books = c.execute("SELECT Title, Author, Book_ID, Borrow_date, Return_date from borrow_history where User = ?", (self.name,)).fetchall()

        for book in books:
            if book[4] != '':
                print(f"Title: {book[0]}\nAuthor: {book[1]}\nID Number: {book[2]}\nDate Borrowed: {book[3]}\nDate Returned: {book[4]}\n")
            elif book[4] == '':
                print(f"Title: {book[0]}\nAuthor: {book[1]}\nID Number: {book[2]}\nDate Borrowed: {book[3]}\nDate Returned: Not yet returned\n")
            
        if books == []:
            print("You haven't borrwed a book yet! Try borrowing")