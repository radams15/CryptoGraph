
class Trade:
    def __init__(self, user, currency_id, unit_price, amount_bought, trade_id=None):
        self.user = user
        self.currency_id = currency_id
        self.unit_price = unit_price
        self.amount_bought = amount_bought
        self.id = trade_id

    def __repr__(self):
        return "{} {} @ £{}".format(self.amount_bought, self.currency_id, self.unit_price)
