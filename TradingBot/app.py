import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_input = request.form["stock"]
        response = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=100,
            prompt=generate_prompt(user_input),
            temperature=0.0,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(user_input):
    return """
    Stock: {}
    Response:""".format(
        user_input.capitalize()
    )