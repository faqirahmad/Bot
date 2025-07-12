import ccxt
import time
import json
from strategy import check_buy_signals, check_sell_signals

with open("config.json") as f:
    config = json.load(f)

exchange = ccxt.gateio({
    'apiKey': config['exchange']['key'],
    'secret': config['exchange']['secret'],
})

symbol = config['exchange']['pair_whitelist'][0]
amount = config['stake_amount']
dry_run = config['dry_run']

in_position = False
buy_price = 0

def fetch_data():
    candles = exchange.fetch_ohlcv(symbol, timeframe='5m', limit=50)
    return {'close': [c[4] for c in candles]}, candles[-1][4]

while True:
    try:
        data, current_price = fetch_data()

        if not in_position and check_buy_signals(data):
            print("📈 سیگنال خرید شناسایی شد.")
            buy_price = current_price if dry_run else float(exchange.create_market_buy_order(symbol, amount)['price'])
            in_position = True

        elif in_position and check_sell_signals(data, buy_price, current_price):
            print("📉 سیگنال فروش یا سود 4٪ شناسایی شد.")
            if not dry_run:
                exchange.create_market_sell_order(symbol, amount)
            in_position = False

        time.sleep(60)

    except Exception as e:
        print("❗ خطا:", e)
        time.sleep(60)
