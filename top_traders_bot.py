"""
Trading bot that buys/sells futures based on the "Top Traders Long/Short Ratio (Positions)". 
"""

import client_wrapper as cw
import config
from threading import Thread
import helpers as h
from time import sleep


def trading_bot():
   """ function that implements the trading strategy """
   while True:
      # loop to constantly check the ratio and buy/sell
      # print when the last check was
      print(f"{h.timeNow()} Was the last check.", end="\r")

      # get the position amount (positive for long, negative for short)
      pos_amt = h.current_position_amount(config.SYMBOL)

      response = cw.futures_top_longshort_position_ratio(symbol=config.SYMBOL, period=config.TIME_FRAME, limit=1)[0]
      ratio = float(response['longShortRatio'])
      
      if ratio > 1:
         if (pos_amt < config.TRADING_AMT):
            # either open a new position or add to the long, to get to the trading amount
            # set the leverage
            cw.futures_change_leverage(symbol=config.SYMBOL, leverage=config.LEVERAGE)
            # execute market order
            price = h.try_market(config.SYMBOL, 'BUY', config.TRADING_AMT - pos_amt)
            h.status(f"BUY order filled: {config.TRADING_AMT} {config.SYMBOL} at {price}")
      
      if ratio < 1:
         if (-pos_amt < config.TRADING_AMT):
            # either open a new position or add to the short, to get to the trading amount
            # set the leverage
            cw.futures_change_leverage(symbol=config.SYMBOL, leverage=config.LEVERAGE)
            # execute market order
            price = h.try_market(config.SYMBOL, 'SELL', config.TRADING_AMT + pos_amt)
            h.status(f"SELL order filled: {config.TRADING_AMT} {config.SYMBOL} at {price}")

      sleep(config.REACTION_TIME)


if __name__ == "__main__":
   """ main thread, that restarts the trading bots thread """
   while True:
      try:
         t1 = Thread(target=trading_bot, args=())
         t1.start()
         t1.join()      # wait till it returns (only when it crashes)
         h.status('Trading bot thread crashed, restarting in a minute.')
         sleep(60)

      except:
         h.status('Main thread crashed.')
