import sqlite3
from hashlib import sha256
from os import path

from Account import Account
from Trade import Trade


class Database:
    ACCOUNT_INIT = """\
CREATE TABLE "Account" (
    "username"	TEXT NOT NULL UNIQUE,
    "pass_hash"	TEXT NOT NULL,
    "name"	TEXT,
    PRIMARY KEY("username")
);
"""

    TRADE_INIT = """\
CREATE TABLE "Trade" (
	"trade_id"	INTEGER NOT NULL UNIQUE,
	"currency_id"	TEXT NOT NULL,
	"unit_price"	REAL NOT NULL,
	"amount_bought"	REAL NOT NULL,
	"user"	TEXT NOT NULL,
	PRIMARY KEY("trade_id" AUTOINCREMENT),
	FOREIGN KEY("user") REFERENCES "Account"("username")
);
"""

    def __init__(self, file="db.sqlite"):
        create_table = False
        if not path.exists(file):
            create_table = True

        self.conn = sqlite3.connect(file)

        if create_table:
            cur = self.conn.cursor()
            for stat in (self.ACCOUNT_INIT, self.TRADE_INIT):
                cur.execute(stat)
            self.conn.commit()

    def add_trade(self, trade):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO Trade VALUES (NULL, ?, ?, ?, ?)", (trade.currency_id, trade.unit_price, trade.amount_bought, trade.user.username))

        self.conn.commit()

    def del_trade(self, trade):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM Trade WHERE trade_id IS ?", (trade.id,))
        self.conn.commit()

    def get_trades(self, account):
        cur = self.conn.cursor()

        trades = cur.execute("SELECT * FROM Trade WHERE Trade.user = ?", (account.username,))

        for raw in trades:
            trade = Trade(account, raw[1], raw[2], raw[3], trade_id=raw[0])
            yield trade

    def add_account(self, name, username, password):
        hash_pass = sha256(password.encode()).hexdigest()

        cur = self.conn.cursor()

        cur.execute("INSERT INTO Account VALUES (?, ?, ?)", (username, hash_pass, name))

        self.conn.commit()

        return self.account_login(username, password)

    def account_login(self, username, password):
        hash_pass = sha256(password.encode()).hexdigest()

        cur = self.conn.cursor()

        out = list(cur.execute("SELECT name, username FROM Account WHERE username IS ? AND pass_hash IS ?", (username, hash_pass)))

        if len(out) == 1:
            return Account(*out[0])
        else:
            return None