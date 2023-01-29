import os
import openai
from flask import Flask, redirect, render_template, request, url_for

from TradingBot.data_analysis import rsi, generate_graph

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        stock = request.form["stock"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(stock),
            temperature=0.6,
            max_tokens=100
        )
        # response.choices[0].text contains the function call
        print(response.choices[0].text)
        call(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def call(response):
    text = response.choices[0].text
    args = text.split(" ")
    if args[0] == "rsi_lookback":
        rsi(args[1], int(args[2]))
    elif args[0] == "gen_graph":
        generate_graph(args[1])

def generate_prompt(stock):
    return """ Call a function with parameters given an input
    
    Input: Generate the RSI Lookback for BitCoin over the last 7 days
    Call:rsi_lookback BTC-USD 7
    Input: Generate the RSI Lookback for Ethereum over the last 18 days
    Call:rsi_lookback ETH-USD 18
    Input: RSI Lookback for BitCoin last 7 days
    Call:rsi_lookback BTC-USD 7
    Input: RSI Lookback for Ethereum last 14 days
    Call:rsi_lookback ETH-USD 7
    Input: RSI Ethereum 8d
    Call:rsi_lookback ETH-USD 8
    Input: Generate graph for Bitcoin for the last 8 days
    Call:gen_graph BTC-USD 
    Input: Graph Tether last 9 days
    Call:gen_graph USDT-USD
    Input: Show the graph for Polygon
    Call:gen_graph MATIC-USD
    Input: Show the moving average for Lido Stacked 
    Call:moving_avg STETH-USD
    Input: {}
    Call:""".format(
        stock.capitalize()
    )

