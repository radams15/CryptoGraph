import datetime
from sys import exit

import gi

from . import Crypto
from .StatusTable import StatusTable
from .Trade import Trade
from .EntryDialog import EntryDialog

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from .Graph import Graph

class MainWindow(Gtk.Window):

    REFRESH_TIMEOUT = 5 # secs

    def __init__(self, db):
        super().__init__()

        self.db = db
        self.account = self.login()

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

        #refresh_button = Gtk.Button(label="Refresh")
        #refresh_button.connect("clicked", self.refresh)

        buy_button = Gtk.Button(label="Buy")
        buy_button.connect("clicked", self.buy)
        buy_button.get_style_context().add_class("suggested-action")

        self.currency_box = Gtk.ComboBoxText()
        for cur in Crypto.get_currencies()[:100]:
            self.currency_box.append_text(cur)
        self.currency_box.set_active(0)

        self.left_header = Gtk.Label("Price Info")
        self.predicted_label = Gtk.Label("Predicted Price: ")
        self.live_label = Gtk.Label("Live Price: ")
        self.change_label = Gtk.Label("Percentage Change: ")
        self.graph.set_vexpand(True)

        self.right_header = Gtk.Label("Account Info")
        self.user_label = Gtk.Label("Username: ")
        self.portfolio_label = Gtk.Label("Current Portfolio: ")
        self.total_label = Gtk.Label("Total Profit/Loss: ")

        self.status_table = StatusTable(self.sell)
        self.status_table.set_vexpand(True)

        header.pack_start(buy_button)

        grid.attach(self.left_header, 0, 1, 2, 1) # item, along, down, width, height
        grid.attach(self.predicted_label, 0, 2, 1, 1)
        grid.attach(self.live_label, 0, 3, 1, 1)
        grid.attach(self.change_label, 0, 4, 1, 1)
        grid.attach(self.currency_box, 0, 5, 2, 1)
        grid.attach(self.graph, 0, 6, 2, 1)

        grid.attach(self.right_header, 2, 0, 2, 2)
        grid.attach(self.user_label, 2, 2, 1, 1)
        grid.attach(self.portfolio_label, 2, 3, 1, 1)
        grid.attach(self.total_label, 2, 4, 1, 1)
        grid.attach(self.status_table, 2, 5, 2, 3)

        grid.set_column_homogeneous(True)

        self.refresh(ref=True)

    def login(self):
        username_box = EntryDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK,
            text="Login"
        )

        username_box.format_secondary_text("Username:")

        username = username_box.run()

        username_box.destroy()

        password_box = EntryDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK,
            text="Login",
            hidden=True
        )

        password_box.format_secondary_text("Password:")

        password = password_box.run()

        if not password or not username:
            exit(1)

        password_box.destroy()

        account = self.db.account_login(username, password)

        if account:
            return account

        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )

        dialog.format_secondary_text("Invalid username or password")
        dialog.run()
        dialog.destroy()
        exit(1)

    def sell(self, data):
        trade = self.db.get_trade(data[-1])

        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Sell?",
        )

        current_price = Crypto.current_price(trade.currency_id)
        dialog.format_secondary_text(
            "Sell {} {} for £{}?".format(trade.amount_bought, trade.currency_id, current_price*trade.amount_bought)
        )
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            self.account = self.db.update_account(self.account)
            profit = current_price*trade.amount_bought
            self.account.money += profit
            self.db.del_trade(trade)
            self.account = self.db.update_account(self.account)
            self.refresh()
            print("Sale completed")
        elif response == Gtk.ResponseType.NO:
            print("Sale cancelled")

        dialog.destroy()

    def buy(self, *args):
        cur = self.currency_box.get_active_text()

        prompt_box = EntryDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Buy?"
        )

        prompt_box.format_secondary_text(
            "Quantity Of {} To Buy:".format(cur)
        )

        response = prompt_box.run()

        if not response:
            return

        try:
            amount = float(response)
            print(amount)
        except ValueError:
            print("Purchase cancelled")
            prompt_box.destroy()
            return

        prompt_box.destroy()

        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Buy?",
        )

        current_price = Crypto.current_price(cur)
        dialog.format_secondary_text(
            "Buy {} {} for £{}?".format(amount, cur, current_price * amount)
        )
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            self.account = self.db.update_account(self.account)
            trade = Trade(self.account, cur, current_price, amount)
            price = current_price * trade.amount_bought
            if(self.account.money < price):
                print("Cannot afford")
            else:
                self.account.money -= price
                self.db.add_trade(trade)
                self.account = self.db.update_account(self.account)
                self.refresh()
                print("Sale completed")
        elif response == Gtk.ResponseType.NO:
            print("Purchase cancelled")

        dialog.destroy()

    def load_account_data(self):
        trades = self.db.get_trades(self.account)

        data = []
        total_profit = 0
        total_expenditure = 0
        for t in trades:
            price = Crypto.current_price(t.currency_id)

            total_expenditure += (t.amount_bought * t.unit_price)
            total_profit += (t.amount_bought * price)

            data.append([t.currency_id, t.amount_bought, t.unit_price, price, t.id])

        self.total_label.set_text("Total Potential Profit/Loss: £{:.2f}".format(total_profit-total_expenditure))
        self.user_label.set_text("User: {}".format(self.account.name))
        self.portfolio_label.set_text("Current Portfolio: £{:.2f}".format(self.account.money))

        self.status_table.refresh(data)

    def refresh(self, *args, ref=False):
        self.change_coin()
        self.load_account_data()

        if ref:
            GObject.timeout_add_seconds(self.REFRESH_TIMEOUT, lambda: self.refresh(ref=True))

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

    def plot(self, cur, hours=1):
        xs = []
        ys = []

        self.graph.title = "Price Of {}".format(cur)

        for date, avg in Crypto.get_since(cur, datetime.datetime.now()-datetime.timedelta(hours=hours)):
            xs.append(date)
            ys.append(avg)

        self.graph.plot_date_axis_1(xs, ys)
