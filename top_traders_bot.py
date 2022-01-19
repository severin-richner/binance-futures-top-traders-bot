"""
Trading bot that buys/sells futures based on the "Top Traders Long/Short Ratio (Positions)". 
"""

import client_wrapper as cw
from config import *
from multiprocessing import Process
import helpers as h
from time import sleep

# check inputs
assert(len(SYMBOLS) == len(TRADING_AMTS) == len(LEVERAGES) == len(TIME_FRAME) == len(REACTION_TIME))


def trading_bot(symbolElement, tradingAmount, leverage, timeFrame, reactionTime):
   """ function that implements the trading strategy """

   coin = symbolElement[0]
   base = symbolElement[1]
   symbol = coin + base

   while True:
      try:
         # loop to constantly check the ratio and buy/sell
         # print when the last check was
         print(f"{h.timeNow()} Was the last check.", end="\r")

         # get the position amount (positive for long, negative for short)
         pos_amt = h.current_position_amount(symbol)

         response = cw.futures_top_longshort_position_ratio(symbol=symbol, period=timeFrame, limit=1)[0]
         ratio = float(response['longShortRatio'])
      
         if ratio > 1:
            if (pos_amt < tradingAmount):
               # either open a new position or add to the long, to get to the trading amount
               # set the leverage
               cw.futures_change_leverage(symbol=symbol, leverage=leverage)
               # execute market order
               price = h.try_market(symbol, 'BUY', tradingAmount - pos_amt)
               h.status(f"BUY order filled: {tradingAmount - pos_amt} {symbol} at {price}")
      
         if ratio < 1:
            if (-pos_amt < tradingAmount):
               # either open a new position or add to the short, to get to the trading amount
               # set the leverage
               cw.futures_change_leverage(symbol=symbol, leverage=leverage)
               # execute market order
               price = h.try_market(symbol, 'SELL', tradingAmount + pos_amt)
               h.status(f"SELL order filled: {tradingAmount + pos_amt} {symbol} at {price}")

         sleep(reactionTime)
         
      except Exception as e:
         h.status(f"Bot for {symbol} crashed! Problem: {e}.\nTrying again in a minute...")
         sleep(60)


if __name__ == "__main__":
   """ main thread, starts the different trading bots """
   try:
      for i in range(len(SYMBOLS)):
         proc = Process(target=trading_bot, args=[SYMBOLS[i], TRADING_AMTS[i], LEVERAGES[i], TIME_FRAME[i], REACTION_TIME[i]] )
         proc.start()
         sleep(2)    # offset the bots to avoid having too many requests at a time

   except:
      h.status('Main thread crashed.')
