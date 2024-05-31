# Book Library Management System

## Overview
This CLI application allows users to manage a book library. Users can sign up, sign in, add books, view available books, borrow books, return borrowed books, view user profiles, and delete users. The application uses SQLAlchemy ORM for database management and adheres to OOP best practices.

## Features
- User Authentication (Sign Up, Sign In, Sign Out)
- Manage Books (Add, View, Edit, Delete)
- Borrow and Return Books
- View and Search Books by Title, Author, Genre
- View and Manage User Profiles
- Integration with Google Books API for book searches

## Project Structure
- `lib/cli.py`: Main CLI script that handles user interactions.
- `lib/helpers.py`: Helper functions for user prompts and menu handling.
- `lib/models/__init__.py`: Database initialization and configuration.
- `lib/models/user.py`: User model with authentication and profile management.
- `lib/models/book.py`: Book model with borrowing and returning functionalities.

## Setup Instructions
1. Clone the repository.
2. Navigate to the project directory.
3. Install dependencies using Pipenv:

   pipenv install

4. Activate the virtual environment

   pipenv shell

5. Run the CLI

   python lib/cli.py

## Usage

- Follow the prompts to sign up or sign in.
- Navigate through the menus to manage books and user profiles.
- Use the help option for a summary of available commands.

## Dependencies

- Python 3.x
- SQLAlchemy
- Requests
- Pipenv

Author

Shane Lee
