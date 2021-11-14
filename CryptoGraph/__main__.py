import gi

from .Database import Database

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .MainWindow import MainWindow

def main():
    db = Database()

    win = MainWindow(db)
    win.show_all()
    Gtk.main()