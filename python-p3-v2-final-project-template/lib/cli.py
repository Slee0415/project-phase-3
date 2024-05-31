from simple_term_menu import TerminalMenu
from helpers import Prompt, hash_password, verify_password
from models import init_db, SessionLocal
from models.user import User
from models.book import Book
from models.history import History
import requests
from datetime import datetime

current_user = None

def display_ascii_art():
    print("""
       .--.                   .---.
   .---|__|           .-.     |~~~|
.--|===|--|_          |_|     |~~~|--.
|  |===|  |'\     .---!~|  .--|   |--|
|%%|   |  |.'\    |===| |--|%%|   |  |
|%%|   |  |\.'\   |   | |__|  |   |  |
|  |   |  | \  \  |===| |==|  |   |  |
|  |   |__|  \.'\ |   |_|__|  |~~~|__|
|  |===|--|   \.'\|===|~|--|%%|~~~|--|
^--^---'--^    `-'`---^-^--^--^---'--'
          
    """)

def display_goodbye_ascii_art():
    print("""
   █████████                        █████ █████                         ███
  ███░░░░░███                      ░░███ ░░███                         ░███
 ███     ░░░   ██████   ██████   ███████  ░███████  █████ ████  ██████ ░███
░███          ███░░███ ███░░███ ███░░███  ░███░░███░░███ ░███  ███░░███░███
░███    █████░███ ░███░███ ░███░███ ░███  ░███ ░███ ░███ ░███ ░███████ ░███
░░███  ░░███ ░███ ░███░███ ░███░███ ░███  ░███ ░███ ░███ ░███ ░███░░░  ░░░ 
 ░░█████████ ░░██████ ░░██████ ░░████████ ████████  ░░███████ ░░██████  ███
  ░░░░░░░░░   ░░░░░░   ░░░░░░   ░░░░░░░░ ░░░░░░░░    ░░░░░███  ░░░░░░  ░░░ 
                                                     ███ ░███              
                                                    ░░██████               
                                                     ░░░░░░                
    """)

def main_menu():
    display_ascii_art()
    options = ["Sign In", "Sign Up", "Exit"]
    selection = Prompt.menu(options)

    if selection == "Sign In":
        sign_in()
    elif selection == "Sign Up":
        sign_up()
    elif selection == "Exit":
        exit_program()

def sign_in():
    global current_user
    username = Prompt.ask("Enter username: ")
    password = Prompt.ask("Enter password: ")
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(user.password, password):
        current_user = user
        session.close()
        user_menu()
    else:
        session.close()
        print("Invalid username or password.")
        main_menu()

def sign_up():
    username = Prompt.ask("Enter username: ")
    password = Prompt.ask("Enter password: ")
    session = SessionLocal()
    new_user = User(username=username, password=hash_password(password))
    session.add(new_user)
    session.commit()
    session.close()
    print(f"User {username} created successfully!")
    main_menu()

def sign_out():
    global current_user
    current_user = None
    main_menu()

def user_menu():
    print("""
 ██████   ██████                               
░░██████ ██████                                
 ░███░█████░███   ██████  ████████   █████ ████
 ░███░░███ ░███  ███░░███░░███░░███ ░░███ ░███ 
 ░███ ░░░  ░███ ░███████  ░███ ░███  ░███ ░███ 
 ░███      ░███ ░███░░░   ░███ ░███  ░███ ░███ 
 █████     █████░░██████  ████ █████ ░░████████
░░░░░     ░░░░░  ░░░░░░  ░░░░ ░░░░░   ░░░░░░░░ 
    """)
    options = ["Book Options", "User Options", "Help", "Sign Out"]
    selection = Prompt.menu(options)

    if selection == "Book Options":
        book_options_menu()
    elif selection == "User Options":
        user_options_menu()
    elif selection == "Help":
        display_help()
    elif selection == "Sign Out":
        sign_out()

def book_options_menu():
    options = ["View Library", "Add Book", "View Borrowed Books", "Edit Book", "Delete Book", "Search Google Books", "View History", "Help", "Sign Out"]
    selection = Prompt.menu(options)

    if selection == "View Library":
        view_library()
    elif selection == "Add Book":
        add_book()
    elif selection == "View Borrowed Books":
        view_borrowed_books()
    elif selection == "Edit Book":
        edit_book()
    elif selection == "Delete Book":
        delete_book()
    elif selection == "Search Google Books":
        search_books()
    elif selection == "View History":
        view_history()
    elif selection == "Help":
        display_help()
    elif selection == "Sign Out":
        sign_out()

def user_options_menu():
    options = ["View Users", "Delete User", "User Profile", "Help", "Sign Out"]
    selection = Prompt.menu(options)

    if selection == "View Users":
        view_users()
    elif selection == "Delete User":
        delete_user()
    elif selection == "User Profile":
        user_profile()
    elif selection == "Help":
        display_help()
    elif selection == "Sign Out":
        sign_out()

def add_book():
    title = Prompt.ask("Enter book title: ")
    author = Prompt.ask("Enter book author: ")
    genre = Prompt.ask("Enter book genre: ")
    try:
        copies = int(Prompt.ask("Enter number of copies: "))
        if not title or not author or not genre or copies < 0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please try again.")
        book_options_menu()
        return

    session = SessionLocal()
    new_book = Book(title=title, author=author, genre=genre, copies=copies)
    session.add(new_book)
    session.commit()
    session.close()
    print(f"Book '{title}' added successfully!")
    book_options_menu()

def view_library():
    query = Prompt.ask("Enter search query (title, author, genre, or leave blank to view all): ")
    session = SessionLocal()
    if query:
        books = session.query(Book).filter((Book.title.contains(query)) | (Book.author.contains(query)) | (Book.genre.contains(query))).all()
    else:
        books = session.query(Book).all()
    
    print("\nSelect a book to borrow!")
    selected_book = display_paginated_list_with_selection(books, detail=True)
    if selected_book:
        borrow_book_by_title(selected_book.title)
    session.close()
    book_options_menu()

def borrow_book_by_title(title):
    session = SessionLocal()
    book = session.query(Book).filter_by(title=title).first()
    if book and book.copies > 0:
        book.copies -= 1
        book.user_id = current_user.id
        session.add(History(user_id=current_user.id, book_id=book.id, action='borrowed', timestamp=datetime.utcnow()))
        session.commit()
        print(f"You have borrowed '{book.title}'.")
    else:
        print("Book not available.")
    session.close()

def view_borrowed_books():
    session = SessionLocal()
    books = session.query(Book).filter_by(user_id=current_user.id).all()
    print("\nSelect a book to return!")
    selected_book = display_paginated_list_with_selection(books, detail=True)
    if selected_book:
        return_book_by_title(selected_book.title)
    session.close()
    book_options_menu()

def return_book_by_title(title):
    session = SessionLocal()
    book = session.query(Book).filter_by(title=title, user_id=current_user.id).first()
    if book:
        book.copies += 1
        book.user_id = None
        session.add(History(user_id=current_user.id, book_id=book.id, action='returned', timestamp=datetime.utcnow()))
        session.commit()
        print(f"You have returned '{book.title}'.")
    else:
        print("You do not have this book.")
    session.close()

def edit_book():
    session = SessionLocal()
    books = session.query(Book).all()
    selected_book = display_paginated_list_with_selection(books, detail=True)
    if selected_book:
        book = session.query(Book).filter_by(title=selected_book.title).first()
        if book:
            new_title = Prompt.ask(f"Enter new title (current: {book.title}): ")
            new_author = Prompt.ask(f"Enter new author (current: {book.author}): ")
            new_genre = Prompt.ask(f"Enter new genre (current: {book.genre}): ")
            try:
                new_copies = int(Prompt.ask(f"Enter new number of copies (current: {book.copies}): "))
                if not new_title or not new_author or not new_genre or new_copies < 0:
                    raise ValueError
            except ValueError:
                print("Invalid input. Please try again.")
                book_options_menu()
                return

            book.title = new_title
            book.author = new_author
            book.genre = new_genre
            book.copies = new_copies
            session.commit()
            print(f"Book '{selected_book.title}' updated successfully!")
        else:
            print("Book not found.")
    session.close()
    book_options_menu()

def delete_book():
    session = SessionLocal()
    books = session.query(Book).all()
    selected_book = display_paginated_list_with_selection(books, detail=True)
    if selected_book:
        book = session.query(Book).filter_by(title=selected_book.title).first()
        if book:
            confirm = Prompt.ask(f"Are you sure you want to delete '{selected_book.title}'? (yes/no): ")
            if confirm.lower() == 'yes':
                session.delete(book)
                session.commit()
                print(f"Book '{selected_book.title}' deleted successfully!")
        else:
            print("Book not found.")
    session.close()
    book_options_menu()

def search_books():
    query = Prompt.ask("Enter search query: ")
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query}")
    books = response.json().get('items', [])
    for book in books:
        volume_info = book.get('volumeInfo', {})
        print(f"Title: {volume_info.get('title')}")
        print(f"Authors: {volume_info.get('authors')}")
        print(f"Published Date: {volume_info.get('publishedDate')}")
        print(f"Description: {volume_info.get('description')}")
        print("-" * 40)
    book_options_menu()

def view_users():
    session = SessionLocal()
    users = session.query(User).all()
    display_paginated_list(users, detail=True, user=True)
    session.close()
    user_options_menu()

def delete_user():
    session = SessionLocal()
    users = session.query(User).all()
    selected_user = display_paginated_list_with_selection(users, detail=True, user=True)
    if selected_user:
        user = session.query(User).filter_by(username=selected_user.username).first()
        if user:
            confirm = Prompt.ask(f"Are you sure you want to delete user '{selected_user.username}'? (yes/no): ")
            if confirm.lower() == 'yes':
                session.delete(user)
                session.commit()
                print(f"User '{selected_user.username}' deleted successfully!")
        else:
            print("User not found.")
    session.close()
    user_options_menu()

def user_profile():
    options = ["Update Username", "Update Password", "Back"]
    selection = Prompt.menu(options)

    if selection == "Update Username":
        update_username()
    elif selection == "Update Password":
        update_password()
    elif selection == "Back":
        user_options_menu()

def update_username():
    new_username = Prompt.ask("Enter new username: ")
    session = SessionLocal()
    current_user.username = new_username
    session.commit()
    session.close()
    print("Username updated successfully!")
    user_options_menu()

def update_password():
    new_password = Prompt.ask("Enter new password: ")
    session = SessionLocal()
    current_user.password = hash_password(new_password)
    session.commit()
    session.close()
    print("Password updated successfully!")
    user_options_menu()

def display_paginated_list(items, page_size=5, detail=False, user=False):
    total_pages = (len(items) + page_size - 1) // page_size
    page = 0

    while True:
        start = page * page_size
        end = start + page_size
        for i, item in enumerate(items[start:end], start=1):
            if detail and user:
                print(f"{i}. Username: {item.username}")
            elif detail:
                print(f"{i}. Title: {item.title}, Author: {item.author}, Genre: {item.genre}, Copies: {item.copies}")
            else:
                print(f"{i}. {item}")

        print(f"\nPage {page + 1} of {total_pages}")

        options = []
        if page > 0:
            options.append("Previous Page")
        if page < total_pages - 1:
            options.append("Next Page")
        options.append("Back to Menu")

        selection = Prompt.menu(options)

        if selection == "Previous Page":
            page -= 1
        elif selection == "Next Page":
            page += 1
        elif selection == "Back to Menu":
            break

def display_paginated_list_with_selection(items, page_size=5, detail=False, user=False):
    total_pages = (len(items) + page_size - 1) // page_size
    page = 0

    while True:
        start = page * page_size
        end = start + page_size
        for i, item in enumerate(items[start:end], start=1):
            if detail and user:
                print(f"{i}. Username: {item.username}")
            elif detail:
                print(f"{i}. Title: {item.title}, Author: {item.author}, Genre: {item.genre}, Copies: {item.copies}")
            else:
                print(f"{i}. {item}")

        print(f"\nPage {page + 1} of {total_pages}")

        options = []
        if page > 0:
            options.append("Previous Page")
        if page < total_pages - 1:
            options.append("Next Page")
        options.extend([str(i + 1) for i in range(len(items[start:end]))])
        options.append("Back to Menu")

        selection = Prompt.menu(options)

        if selection == "Previous Page":
            page -= 1
        elif selection == "Next Page":
            page += 1
        elif selection.isdigit():
            return items[start + int(selection) - 1]
        elif selection == "Back to Menu":
            break

def view_history():
    session = SessionLocal()
    history = session.query(History).filter_by(user_id=current_user.id).all()
    for record in history:
        action = "borrowed" if record.action == 'borrowed' else "returned"
        book = session.query(Book).filter_by(id=record.book_id).first()
        timestamp = record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Book '{book.title}' was {action} on {timestamp}.")
    session.close()
    book_options_menu()

def display_help():
    print("""
    Help - Book Library Management System
    
    Book Menu Options:
    - View Library: View and search books in the library.
    - Add Book: Add a new book to the library.
    - View Borrowed Books: View and return books you have borrowed.
    - Edit Book: Edit details of a book you have added.
    - Delete Book: Delete a book you have added.
    - Search Google Books: Search for books using the Google Books API.
    - View History: View your borrowing and returning history.
    - Help: Display this help message.
    - Sign Out: Sign out of your account.
    
    User Menu Options:
    - View Users: View all users in the system.
    - Delete User: Delete a user from the system.
    - User Profile: Update your username or password.
    - Help: Display this help message.
    - Sign Out: Sign out of your account.

    """)
    input("Press Enter to return to the menu...")
    if current_user:
        user_menu()
    else:
        main_menu()

def exit_program():
    display_goodbye_ascii_art()
    exit()

def main():
    init_db()
    while True:
        main_menu()

if __name__ == "__main__":
    main()
