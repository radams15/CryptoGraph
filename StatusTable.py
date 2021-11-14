import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StatusTable(Gtk.ScrolledWindow):
    def __init__(self, row_handler):
        super().__init__()

        self.row_handler = row_handler

        col_titles = "Name", "Bought", "Original Price (£)", "Current Price (£)", "Original Value (£)", "Current Value (£)", "Possible Profit (£)"
        self.store = Gtk.ListStore(str, str, str, str, str, str, str, int) # last int is trade ID

        self.view = Gtk.TreeView(model=self.store)
        for i, column_title in enumerate(col_titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.view.append_column(column)

        self.view.connect("row-activated", self.row_clicked)


        self.add(self.view)

    def row_clicked(self, widget, row, col):
        model = widget.get_model()
        data = list(model[row])

        self.row_handler(data)

    def refresh(self, data):
        self.store.clear()
        for (name, num, bought_price, current_price, id) in data:
            self.store.append([name, "{:.2f}".format(num), "{:.2f}".format(bought_price), "{:.2f}".format(current_price), "{:.2f}".format(bought_price*num), "{:.2f}".format(current_price*num), "{:.2f}".format((current_price*num)-(bought_price*num)), id])