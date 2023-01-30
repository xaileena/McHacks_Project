# TradingBot
*Team: Zichen Gao, Naomie Lo, Aileena Xie & Loïc Duchesne*

This bot was created during **McHack 2023**, and **winner of the Tower Research Capital LLC. Challenge**.

This chatbot can provide responses to natural language inputs about various cryptocurrency statistics. It can give current information about a particular cryptocurrency, plot graphs with or without indicators or provide general information. The user inputs a question about crypto, for example: "show the RSI call back for crypto in last month" and the bot will plot the corresponding RSI graph.

## What is currently implemented:
The model was structured in 3 parts.

- The Natural Language Model
- The data mining & technical analysis backend
- The frontend

The chatbot, albeit easily modular is limited by the functions we had time to implement.

### Natural Language Model
Our NLP model makes use of OpenAI's API. We opted to fine tune an existing model, since the results were beyond our expectations. This model is restricted by the functions that we had time to implement, but is very modular in terms of adding future functions.

Most of the model can be found in app.py.

### Technical Analysis
We first needed to implement the data collection component for this backend. We did this by using the yfinance package. This would allow us to stream live data about multiple cryptos directly to our technical analysis models.

After we set up the data collection, we decided we wanted to implement some models ourselves as a proof of concept, instead of using one of the many packages available that already contain the technical analysis markers. This allowed us to understand the algorithm behind the technical analysis markers.

The way our backend was developed allows us to easily add more markers or just directly implement one of the public technical analysis packages.

### Front-end
Our front-end was developed using Flask, HTML & CSS. It is a simple chat box where you can write any questions and the answer will either be displayed as text or a graph will open depending on the question.

## Future plans
The next steps for this bot can be, although not limited to:

- Extensively train the model with additional data sets
- Either implement additional technical analysis markers or make use of public packages
- Develop the ability to offer trading strategies using further AI techniques based on historical data & current markers
- Upgrade the front-end components
- Move the host to the cloud


