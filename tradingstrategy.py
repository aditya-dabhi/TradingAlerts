import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import date, timedelta
from stocks_list_data import get_nifty_100_stocks
yf.pdr_override()


def RSI(data, window=14, adjust=False):
    delta = data['close'].diff(1).dropna()
    loss = delta.copy()
    gains = delta.copy()

    gains[gains < 0] = 0
    loss[loss > 0] = 0

    gain_ewm = gains.ewm(com=window - 1, adjust=adjust).mean()
    loss_ewm = abs(loss.ewm(com=window - 1, adjust=adjust).mean())

    RS = gain_ewm / loss_ewm
    RSI = 100 - 100 / (1 + RS)

    return RSI


def trading_strategy_1():
    stocks_list = get_nifty_100_stocks()
    stocks_data = {}
    for stock in stocks_list:
        stock_data = pdr.get_data_yahoo(stock + ".NS", start="2023-01-01", end=date.today() + timedelta(days=1))
        data = pd.DataFrame(index=stock_data.index)
        data['open'] = stock_data['Open']
        data['high'] = stock_data['High']
        data['low'] = stock_data['Low']
        data['close'] = stock_data['Close']
        stocks_data[stock] = data

    nifty_data = pdr.get_data_yahoo("^CNX100", start="2023-01-01", end=date.today() + timedelta(days=1))
    nifty = pd.DataFrame(index=stocks_data['ITC'].index)
    nifty['open'] = nifty_data['Open']
    nifty['high'] = nifty_data['High']
    nifty['low'] = nifty_data['Low']
    nifty['close'] = nifty_data['Close']

    for stock in stocks_list:
        stocks_data[stock]["21_EMA"] = stocks_data[stock]['close'].ewm(span=21).mean()
        stocks_data[stock]["rsi"] = RSI(stocks_data[stock], 14, False)
        price_trigger = [0, 0]
        rs_index = [0] * 20
        for i in range(2, len(stocks_data[stock])):
            if stocks_data[stock].iloc[i,3] > stocks_data[stock].iloc[i-1,1] and stocks_data[stock].iloc[i-1,3] > stocks_data[stock].iloc[i-2,1]:
                price_trigger.append(1)
            else:
                price_trigger.append(0)
            if i >= 20:
                rs_index.append(((stocks_data[stock].iloc[i, 3] / stocks_data[stock].iloc[i - 20, 3]) / (
                            nifty.iloc[i, 3] / nifty.iloc[i - 20, 3])) - 1)
        stocks_data[stock]['price_trigger'] = price_trigger
        stocks_data[stock]['rs_index'] = rs_index

    buy_stocks = []
    for stock in stocks_list:
        if stocks_data[stock].iloc[-1,6] == 1 and stocks_data[stock].iloc[-1,3] > stocks_data[stock].iloc[-1,4] and stocks_data[stock].iloc[-1,5] >= 0.5 and stocks_data[stock].iloc[i,3] > stocks_data[stock].iloc[i,0]:
            buy_stocks.append(stock)

    return buy_stocks