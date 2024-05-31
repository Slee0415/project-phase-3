from simple_term_menu import TerminalMenu
import hashlib

class Prompt:
    @staticmethod
    def ask(question):
        return input(question)

    @staticmethod
    def menu(options):
        terminal_menu = TerminalMenu(
            options, skip_empty_entries=True, menu_cursor_style=("fg_purple", "bold"), menu_cursor=("◈ "), menu_highlight_style=("fg_purple", "standout")
        )
        menu_entry_index = terminal_menu.show()
        return options[menu_entry_index]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(hashed_password, user_password):
    return hashed_password == hashlib.sha256(user_password.encode()).hexdigest()
