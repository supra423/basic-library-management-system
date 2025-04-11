from library_management_system import Library
from user_function import User

def main():
    
    library = Library()
    
    name = input("\nPlease enter your name!\n")
    user = User(name)

    while True:

        options = [ "\n"
            "1. Add a book",
            "2. Remove a book",
            "3. Search a book",
            "4. Show all books",
            "5. Borrow a book", 
            "6. Return a book",
            "7. Display your borrowed books",
            "0. Exit"
        ]

        print(*options, sep='\n')

        choice = input("Please choose an option!\n")

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.remove_book()
        elif choice == "3":
            library.search_book()
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            user.borrow_book()
        elif choice == "6":
            user.return_book()
        elif choice == "7":
            user.display_borrowed_books()
        elif choice == "0":
            break
        else:
            print("Invalid choice please choose another number!") 

if __name__ == "__main__":
    main()