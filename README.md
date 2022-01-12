# Binance Futures Top Traders Ratio Bot

This is a very simple crypto trading bot, that trades perpetual Futures using the Binance API. It only uses one simple indicator as the strategy, which is the "Top Traders Long/Short Ratio (Positions)" under the "Trading Data" section of a currency pair.

The bot simply trades with the so called "top traders", meaning:

_Long/Short Ratio > 1:_ ***long***

_Long/Short Ratio < 1:_ ***short***

(The bot can also be connected to a **Telegram Bot** connected to a specific chat to send updates to. More on how to get the token and the chat ID, see [here](https://core.telegram.org/bots).)

## Setup

The settings can be adjusted in the **config.py** file. To start the bot, run the main script **top_traders_bot.py** with python. Make sure that all the files are in the same directory and the necessary packets are installed:

`pip install python-binance requests`

## Disclaimer

This bot is solely a project for fun and is not a profitable trading strategy. _No guarantees about the working of the code. Use at your own risk._
