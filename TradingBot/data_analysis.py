import matplotlib.pyplot as plt
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
import datetime

def plot():
    #gather data
    choice = input("Write a stock symbol: ")
    choice = choice.upper()
    data = yf.download(tickers=choice, period = "5d", interval = "15m", rounding= True)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,open = data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name = "market data"))
    fig.update_layout(title = choice + " share price", yaxis_title = "Stock Price (USD)")
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
    dict(count=45, label="45m", step="minute", stepmode="backward"),
    dict(count=1, label="1h", step="hour", stepmode="backward"),
    dict(count=6, label="6h", step="hour", stepmode="backward"),
    dict(step="all")
    ])
    )
    )
    fig.show()

#plot RSI indicator lookback
def rsi():
    
    return

crypto_lst = ["btc-usd", "eth-usd", "usdt-usd", "bnb-usd", "usdc-usd","xrp-usd", "busd-usd",
              "ada-usd", "doge-usd","matic-usd", "sol-usd", "dot-usd", "avax-usd", "shib-usd", "wtrx-usd", "ltc-usd"]

def biggest_loser(time):
    losers_lst = {}

    today = datetime.date.today() - datetime.timedelta(days=1)
    timeBackwards = today- datetime.timedelta(days=time)
    today = str(today) + " 00:00:00+00:00"
    month = str(timeBackwards) + " 00:00:00+00:00"

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="6mo")
        closehist = hist["Close"]
        end = closehist.loc[today]
        start = closehist.loc[month]
        losers_lst[crypto] = end-start

    return min(losers_lst, key=losers_lst.get)

print(biggest_loser(30))
