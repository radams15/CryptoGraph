import cryptocompare as cc
from datetime import datetime as dt

DEFAULT_REF = "GBP"
EXCHANGE = "CCCAGG"

def get_all(currency, ref=DEFAULT_REF):
    return get_since(currency, dt.now(), ref)

def get_to(currency, start, ref=DEFAULT_REF):
    raw = cc.get_historical_price_day(currency, ref, exchange=EXCHANGE, toTs=start)

    for day in raw:
        date = dt.fromtimestamp(day["time"])
        high = day["high"]
        low = day["low"]
        avg = (high + low) / 2

        yield [date, avg]
def get_since(currency, start, ref=DEFAULT_REF):
    raw = cc.get_historical_price_minute(currency, ref, exchange=EXCHANGE, toTs=dt.now())

    for day in raw:
        date = dt.fromtimestamp(day["time"])

        if date < start:
            continue

        high = day["high"]
        low = day["low"]
        avg = (high + low) / 2

        yield [date, avg]

def current_price(currency, ref=DEFAULT_REF):
    return cc.get_price(currency, ref)[currency][ref]

def previous_price_min(currency, ago=1, ref=DEFAULT_REF):
    data = cc.get_historical_price_minute(currency, ref, limit=ago, exchange=EXCHANGE)[-1]

    avg = (data["low"]+data["high"])/2

    return avg

def get_currencies():
    return [
        "BTC",
        "ETH"
    ]

def predict_future(currency, mins=1, ref=DEFAULT_REF):
    past = previous_price_min(currency, 1, ref)
    current = current_price(currency, ref)

    change = current-past

    new = current+(change*mins)

    return new