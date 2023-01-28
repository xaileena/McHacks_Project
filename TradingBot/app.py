import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        stock = request.form["stock"]
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=100,
            prompt=generate_prompt(stock),
            temperature=0.0,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(Stock):
    return """Show the market trends from the last 5 days, and decide if it is worth investing. If it is positive, it is worth investing.
    If it is negative, it is not worth investing.


Stock: Apple
Response: There is an increase of 5.67 percent from the last 5 days. It could be a good idea to invest in.
Stock: Pepsi
Response: There is a decrease of 0.31 percent from the last 5 days. It might not be a good idea to invest in.
Stock: Petco
Response: There is an increase of 6.82 percent from the last 5 days. It could be a good idea to invest in.
Stock: Swoop
Response: There is a decrease of 1.47 percent from the last 5 days. It might not be a good idea to invest in.

Stock: {}
Response:""".format(
        Stock.capitalize()
    )