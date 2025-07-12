import ccxt
import talib
import numpy as np

def check_buy_signals(data):
    close = np.array(data['close'])
    ema9 = talib.EMA(close, timeperiod=9)
    ema21 = talib.EMA(close, timeperiod=21)
    rsi = talib.RSI(close, timeperiod=14)
    return ema9[-1] > ema21[-1] and ema9[-2] <= ema21[-2] and rsi[-1] > 50

def check_sell_signals(data, buy_price, current_price):
    profit = (current_price - buy_price) / buy_price
    close = np.array(data['close'])
    ema9 = talib.EMA(close, timeperiod=9)
    ema21 = talib.EMA(close, timeperiod=21)
    return profit >= 0.04 or (ema9[-1] < ema21[-1] and ema9[-2] >= ema21[-2])
