import matplotlib.pyplot as plt
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
import datetime
import numpy as np


def generate_plot(stock_symbol):
    # gather data
    stock_symbol = stock_symbol.upper()
    data = yf.download(tickers=stock_symbol, period="5d", interval="15m", rounding=True)
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"],
                       name="market data"))
    fig.update_layout(title=stock_symbol + " share price", yaxis_title="Stock Price (USD)")
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
#generate_plot("btc-usd")

#Indicators Graphs
def rsi(stock_symbol, time):
    #TAKEN FROM https://www.qmr.ai/relative-strength-index-rsi-in-python/
    symbol = yf.Ticker(stock_symbol)
    df_btc = symbol.history(interval="1d",period="12mo")

    change = df_btc["Close"].diff()
    change.dropna(inplace=True)

    change_up = change.copy()
    change_down = change.copy()

    change_up[change_up<0] = 0
    change_down[change_down>0] = 0

    # Verify that we did not make any mistakes
    change.equals(change_up+change_down)

    # Calculate the rolling average of average up and average down
    avg_up = change_up.rolling(time).mean()
    avg_down = change_down.rolling(time).mean().abs()

    rsi = 100 * avg_up / (avg_up + avg_down)

    # Set the theme of our chart
    #plt.style.use('fivethirtyeight')

    # Make our resulting figure much bigger
    plt.rcParams['figure.figsize'] = (20, 20)

    # Create two charts on the same figure.
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

    # First chart:
    # Plot the closing price on the first chart
    ax1.plot(df_btc['Close'], linewidth=2)
    ax1.set_title(stock_symbol + " price")

    # Second chart
    # Plot the RSI
    ax2.set_title('Relative Strength Index')
    ax2.plot(rsi, color='orange', linewidth=1)
    # Add two horizontal lines, signalling the buy and sell ranges.
    # Oversold
    ax2.axhline(30, linestyle='--', linewidth=1.5, color='green')
    # Overbought
    ax2.axhline(70, linestyle='--', linewidth=1.5, color='red')

    # Print the result
    plt.show()

#rsi("btc-usd", 7)

def moving_avg(stock_symbol, time):
    symbol = yf.Ticker(stock_symbol)
    df_btc = symbol.history(interval="1d",period="12mo")

    change = df_btc["Close"]
    change.dropna(inplace=True)

    change_up = change.copy()

    change_up[change_up<0] = 0

    # Verify that we did not make any mistakes
    change.equals(change_up)

    # Calculate the rolling average of average up and average down
    avg_up = change_up.rolling(time).mean()

    rsi = avg_up

    # Take a look at the 20 oldest datapoints
    rsi.head(20)

    # Set the theme of our chart
    #plt.style.use('fivethirtyeight')

    # Make our resulting figure much bigger
    plt.rcParams['figure.figsize'] = (20, 20)

    # Create two charts on the same figure.
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)

    # First chart:
    # Plot the closing price on the first chart
    ax1.plot(df_btc['Close'], linewidth=2)
    #ax1.set_title(stock_symbol + " price")

    # Second chart
    # Plot the RSI
    ax1.set_title('Moving Average ' + stock_symbol)
    ax1.plot(rsi, color='orange', linewidth=1)
    # Add two horizontal lines, signalling the buy and sell ranges.
    # Oversold
    ax1.axhline(30, linestyle='--', linewidth=1.5, color='green')
    # Overbought
    ax1.axhline(70, linestyle='--', linewidth=1.5, color='red')

    # Print the result
    plt.show()

#moving_avg("btc-usd", 14)
def stochastic(stock_symbol, time):
    symbol = yf.Ticker(stock_symbol)
    df = symbol.history(interval="1d",period="12mo")

    df_low = df["Low"]
    df_low.dropna(inplace=True)
    df_high = df["High"]
    df_high.dropna(inplace=True)

    df_close = df["Close"]
    df_close.dropna(inplace=True)

    L14 = df_low.rolling(window=time).min()
    L14.dropna(inplace=True)
    H14 = df_high.rolling(window=time).max()
    H14.dropna(inplace=True)

    stochastic = 100 * ((df_close-L14)/(H14-L14))

    # Set the theme of our chart
    plt.style.use('fivethirtyeight')

    # Make our resulting figure much bigger
    plt.rcParams['figure.figsize'] = (20, 20)

    # Create two charts on the same figure.
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 4, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (5,0), rowspan = 4, colspan = 1)

    # First chart:
    # Plot the closing price on the first chart
    ax1.plot(df['Close'], linewidth=2)
    ax1.set_title(stock_symbol + " price")

    # Second chart
    # Plot the RSI
    ax2.set_title('Stochastic Oscillator')
    ax2.plot(stochastic, color='orange', linewidth=1)

    # Print the result
    plt.show()

#stochastic('wtrx-usd', 1)


crypto_lst = ["btc-usd", "eth-usd", "usdt-usd", "bnb-usd", "usdc-usd", "xrp-usd", "busd-usd",
              "ada-usd", "doge-usd", "matic-usd", "sol-usd", "dot-usd", "avax-usd", "shib-usd", "wtrx-usd", "ltc-usd"]

#data analysis
def biggest_loser(time):
    #biggest difference in opening and closing value
    losers_lst = {}

    today = datetime.date.today() - datetime.timedelta(days=0)
    timeBackwards = today - datetime.timedelta(days=time)
    endDate = str(today) + " 00:00:00+00:00"
    startDate = str(timeBackwards) + " 00:00:00+00:00"

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="max")
        if(len(hist) >= time):
            closehist = hist["Close"]
            end = closehist.loc[endDate]
            start = closehist.loc[startDate]
            losers_lst[crypto] = end - start

    return min(losers_lst, key=losers_lst.get)

#print(biggest_loser(365))

def max_gainer(time):
    max_gainer = {}

    today = datetime.date.today() - datetime.timedelta(days=1)
    timeBackwards = today - datetime.timedelta(days=time)
    endDate = str(today) + " 00:00:00+00:00"
    startDate = str(timeBackwards) + " 00:00:00+00:00"

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="max")
        if(len(hist) >= time):
            closehist = hist["Close"]
            end = closehist.loc[endDate]
            start = closehist.loc[startDate]
            max_gainer[crypto] = end - start

    return max(max_gainer, key=max_gainer.get)

def get_stat(stock_symbol, pierod, type_search):
    if type_search == "Open" or type_search == "Close" or type_search == "High" or type_search == "Low" or type_search == "Volume":
        #string (kind of crypto) , int ("month = 30", "year = 365","day = 1"), string ("High", "Low",...)
        data_dict = {}
        get_crypt = yf.Ticker(stock_symbol)
        hist = get_crypt.history(period="max")
        typeLst = hist[type_search]

        for i in range(0,len(hist), pierod):
            if(i < len(hist)):
                getTime = datetime.date.today() - datetime.timedelta(days=i)
                getTime = str(getTime) + " 00:00:00+00:00"
                data_dict[getTime] = typeLst.loc[getTime]

        return str(max(data_dict, key=data_dict.get))[0:10]
    else:
        return "invalid measure search, try 'High', 'Low', 'Close'"

print(get_stat("btc-usd", 7, "Adj Close"))
def highest_volume(date):
    check_date = datetime.date.today() - datetime.timedelta(days=date)
    check_date = str(check_date) + " 00:00:00+00:00"

    highest_vol = 0
    highest_vol_crypto = " "

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="max")
        vol_values = hist["Volume"]
        vol = vol_values.loc[check_date]

        if (vol > highest_vol):
            highest_vol = vol
            highest_vol_crypto = crypto

    return highest_vol_crypto



def volatlity(period):
    voltality_lst = {}

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period=(str(period)+"d"))
        lowhist = hist["Low"]
        #print(lowhist)
        hihist = hist["High"]
        #print(hihist)
        difflist = []
        for i in range(period):
            today = datetime.date.today() - datetime.timedelta(days=i)
            currentTime = str(today) + " 00:00:00+00:00"
            #print(currentTime)
            difflist.append(hihist.loc[currentTime]-lowhist.loc[currentTime])
        voltality_lst[crypto] = (sum(difflist)/len(difflist)) / 100

    return voltality_lst

#print(volatlity(30))