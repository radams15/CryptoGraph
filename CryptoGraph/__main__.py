import gi
from sys import argv

from .Database import Database

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .MainWindow import MainWindow

def main():
    db = Database()

    if len(argv) > 1 and argv[1] == "adduser":
        username = input("Username: ")
        password = input("Password: ")
        password1 = input("Password (Repeat): ")
        name = input("Real Name: ")
        if password == password1:
            db.add_account(name, username, password)
        else:
            print("Passwords do not match!")
    else:
        win = MainWindow(db)
        win.show_all()
        Gtk.main()