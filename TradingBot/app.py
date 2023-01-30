import os

import openai
from flask import Flask, redirect, render_template, request, url_for

from TradingBot.data_analysis import rsi, generate_plot, moving_avg, stochastic, max_gainer, biggest_loser, get_stat, \
    volatlity

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
        text_resp = call(response)
        return redirect(url_for("index", result=text_resp))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def call(response):
    text = response.choices[0].text
    args = text.split(" ")
    print(args)
    if len(args) < 1:
        return "I don't know the answer to that!"
    elif args[0] == "rsi_lookback" and len(args) == 3:
        rsi(args[1], int(args[2]))
    elif args[0] == "gen_graph" and len(args) == 2:
        generate_plot(args[1])
    elif args[0] == "moving_avg" and len(args) == 3:
        moving_avg(args[1], int(args[2]))
    elif args[0] == "stochastic" and len(args) == 3:
        stochastic(args[1], int(args[2]))
    elif args[0] == "max_gainer" and len(args) == 2:
        return "The biggest gainer in the last " + args[1] + " days is " + max_gainer(int(args[1]))
    elif args[0] == "biggest_loser" and len(args) == 2:
        return "The biggest loser is " + biggest_loser(int(args[1]))
    elif args[0] == "get_stats" and len(args) == 4:
        return "The time at which " + args[1] + " was the " + args[3].lower() + "est over a period of " + args[2] \
            + " days is on " + get_stat(args[1], int(args[2]), args[3])
    elif args[0] == "volatility" and len(args) == 2:
        volatlity(int(args[1]))
    else:
        return "I don't know the answer to that!"
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
    Input: Show the moving average for Lido Stacked for the past 2 days
    Call:moving_avg STETH-USD 2
    Input: Display moving avg BTC for 6 days
    Call:moving_avg BTC-USD 6
    Input: Show the stochastic for Polkadot for the past 2 days
    Call:stochastic DOT-USD 2
    Input: Display stochastic Wrapped Tron for 6 days
    Call:stochastic WTRX-USD 6
    Input: Find which crypto gained the most in the last 2 months
    Call:max_gainer 60
    Input: What crypto improved the most last 8 days
    Call:max_gainer 8
    Input: Max gainer in the past 1 week
    Call:max_gainer 7
    Input: Find the which crypto gained the least in the last 6 months
    Call:biggest_loser 180
    Input: What crypto lost the most last 8 days
    Call:biggest_loser 8
    Input: Biggest loser in the past 1 week
    Call:biggest_loser 7
    Input: Which month was the highest gainer for bitcoin?
    Call:get_stats BTC-USD 30 High
    Input: What week did Ethereum gain the highest?
    Call:get_stats ETH-USD 7 High
    Input: Which month was the lowest gainer for bitcoin?
    Call:get_stats BTC-USD 30 Low
    Input: In what week did Polkadot lose the most?
    Call:get_stats DOT-USD 7 Low
    Input: Get the volatility of all stocks for past 2 weeks
    Call:volatility 14
    Input: What is the volatility of BitCoin for the past month
    Call:volatility 30
    Input:{}
    Call:""".format(
        stock.capitalize()
    )

