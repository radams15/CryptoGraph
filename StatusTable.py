import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StatusTable(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()

        col_titles = "Name", "Each (£)", "Bought", "Value (£)", "Possible Profit (£)"
        self.store = Gtk.ListStore(str, float, float, float, float) # Name, price each, num bought, value, profit

        self.view = Gtk.TreeView(model=self.store)
        for i, column_title in enumerate(col_titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.view.append_column(column)


        self.add(self.view)

        self.refresh()

    def refresh(self):
        for (name, num, price, original) in self.get_data():
            self.store.append([name, round(price, 2), round(num, 2), round(price*num, 2), round(original-(price*num), 2)])

    def get_data(self):
        return [ # list of [name, number bought, price, original_cost]
            ["BTC", 1.1, 47296, 31000],
            ["ETH", 0.15, 37547, 50040]
        ]