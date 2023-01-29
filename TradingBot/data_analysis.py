import matplotlib.pyplot as plt
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
import datetime


def plot():
    # gather data
    choice = input("Write a stock symbol: ")
    choice = choice.upper()
    data = yf.download(tickers=choice, period="5d", interval="15m", rounding=True)
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"],
                       name="market data"))
    fig.update_layout(title=choice + " share price", yaxis_title="Stock Price (USD)")
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

#Indicators Graphs
def rsi(stock_symbol, time):
    #TAKEN FROM https://www.qmr.ai/relative-strength-index-rsi-in-python/
    symbol = yf.Ticker(stock_symbol)
    df_btc = symbol.history(interval="1d",period="12mo")
    print(df_btc)

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
    
    # Take a look at the 20 oldest datapoints
    rsi.head(20)
    
    # Set the theme of our chart
    plt.style.use('fivethirtyeight')
    
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

#rsi("btc-usd", 3)

crypto_lst = ["btc-usd", "eth-usd", "usdt-usd", "bnb-usd", "usdc-usd", "xrp-usd", "busd-usd",
              "ada-usd", "doge-usd", "matic-usd", "sol-usd", "dot-usd", "avax-usd", "shib-usd", "wtrx-usd", "ltc-usd"]



#data analysis
def biggest_loser(time):
    losers_lst = {}

    today = datetime.date.today() - datetime.timedelta(days=1)
    timeBackwards = today - datetime.timedelta(days=time)
    today = str(today) + " 00:00:00+00:00"
    month = str(timeBackwards) + " 00:00:00+00:00"

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="6mo")
        closehist = hist["Close"]
        end = closehist.loc[today]
        start = closehist.loc[month]
        losers_lst[crypto] = end - start

    return min(losers_lst, key=losers_lst.get)


def max_gainer(time):
    max_gainer = {}

    today = datetime.date.today() - datetime.timedelta(days=1)
    timeBackwards = today - datetime.timedelta(days=time)
    today = str(today) + " 00:00:00+00:00"
    month = str(timeBackwards) + " 00:00:00+00:00"

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="6mo")
        closehist = hist["Close"]
        end = closehist.loc[today]
        start = closehist.loc[month]
        max_gainer[crypto] = end - start

    return max(max_gainer, key=max_gainer.get)


def highest_volume(date):
    check_date = datetime.date.today() - datetime.timedelta(days=date)
    check_date = str(check_date) + " 00:00:00+00:00"

    highest_vol = 0
    highest_vol_crypto = " "

    for crypto in crypto_lst:
        get_crypt = yf.Ticker(crypto)
        hist = get_crypt.history(period="1mo")
        vol_values = hist["Volume"]
        vol = vol_values.loc[check_date]

        if (vol > highest_vol):
            highest_vol = vol
            highest_vol_crypto = crypto

    return highest_vol_crypto


'''
def volatlity(timeback, timeframe):
voltality_lst = {}

today = datetime.date.today() - datetime.timedelta(days=1)
timeBackwards = today- datetime.timedelta(days=timeframe)
today = str(today) + " 00:00:00+00:00"
month = str(timeBackwards) + " 00:00:00+00:00"



for crypto in crypto_lst:
    get_crypt = yf.Ticker(crypto)
    hist = get_crypt.history(period="1mo")
    closehist = hist["Close"]
    end = closehist.loc[today]
    start = closehist.loc[month]
    losers_lst[crypto] = end-start
'''
