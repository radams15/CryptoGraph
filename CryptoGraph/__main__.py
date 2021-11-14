import gi
from sys import exit

from .Database import Database

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .MainWindow import MainWindow

def main():
    db = Database()
    account = db.account_login("rhys", "rhysadams")

    if account == None:
        print("Invalid Login")
        exit(1)

    win = MainWindow(db, account)
    win.show_all()
    Gtk.main()