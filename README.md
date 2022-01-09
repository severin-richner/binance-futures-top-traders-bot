# Binance Futures Top Traders Ratio Bot

This is a very simple crypto trading bot, that trades perpetual Futures using the Binance API. It only uses one simple indicator as the strategy, which is the "Top Traders Long/Short Ratio (Positions)" under the "Trading Data" section of a currency pair.

The bot simply trades with the so called "top traders", meaning:

_Long/Short Ratio_ > 50: **long**

_Long/Short Ratio_ < 50: **short**

## Disclaimer

This bot is solely a project for fun and is not a profitable trading strategy. Use at your own risk.

## Setup

The settings can be adjusted in the "config.py" file.
