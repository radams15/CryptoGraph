import datetime

import gi

import Crypto
from StatusTable import StatusTable

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from Graph import Graph

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.graph = Graph()

        self.connect("delete-event", Gtk.main_quit)
        self.set_default_size(1600, 900)
        self.set_title("Crypto Tracker")

        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        self.set_titlebar(header)

        grid = Gtk.Grid()
        self.add(grid)

        grid.set_border_width(10)

        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.connect("clicked", self.change_coin)

        self.currency_box = Gtk.ComboBoxText()
        for cur in Crypto.get_currencies()[:100]:
            self.currency_box.append_text(cur)
        self.currency_box.set_active(0)

        self.left_header = Gtk.Label("Price Info")
        self.predicted_label = Gtk.Label("Predicted Price: ")
        self.live_label = Gtk.Label("Live Price: ")
        self.change_label = Gtk.Label("Percentage Change: ")
        self.graph.set_vexpand(True)

        self.status_table = StatusTable()
        self.status_table.set_vexpand(True)

        grid.attach(self.left_header, 0, 1, 2, 1) # item, along, down, width, height
        grid.attach(self.predicted_label, 0, 2, 1, 1)
        grid.attach(self.live_label, 0, 3, 1, 1)
        grid.attach(self.change_label, 0, 4, 1, 1)
        grid.attach(refresh_button, 0, 5, 1, 1)
        grid.attach(self.currency_box, 1, 5, 1, 1)
        grid.attach(self.graph, 0, 6, 2, 1)
        grid.attach(self.status_table, 2, 0, 1, 7)

        grid.set_column_homogeneous(True)

        self.change_coin()

    def change_coin(self, *args):
        cur = self.currency_box.get_active_text()

        if not cur:
            return

        prev = Crypto.previous_price_min(cur)
        current = Crypto.current_price(cur)
        future = Crypto.predict_future(cur)
        change = ((current-prev)/future)*100

        self.left_header.set_text("Price Info ({})".format(cur))
        self.predicted_label.set_text("Predicted Price: £{:.2f}".format(future))
        self.live_label.set_text("Live Price: £{:.2f}".format(current))
        self.change_label.set_text("Percentage Change: {:.2f}%".format(change))

        self.plot(cur)

    def plot(self, cur, days=30):
        xs = []
        ys = []

        self.graph.title = "Price Of {}".format(cur)

        for date, avg in Crypto.get_since(cur, datetime.datetime.now()-datetime.timedelta(days=days)):
            xs.append(date)
            ys.append(avg)

        self.graph.plot_date_axis_1(xs, ys)
