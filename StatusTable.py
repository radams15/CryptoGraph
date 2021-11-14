import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StatusTable(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()

        col_titles = "Name", "Bought", "Original Price (£)", "Current Price (£)", "Original Value (£)", "Current Value (£)", "Possible Profit (£)"
        self.store = Gtk.ListStore(str, float, float, float, float, float, float)

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

        print(data)

    def refresh(self, data):
        self.store.clear()
        for (name, num, bought_price, current_price) in data:
            self.store.append([name, num, bought_price, current_price, bought_price*num, current_price*num, (current_price*num)-(bought_price*num)])