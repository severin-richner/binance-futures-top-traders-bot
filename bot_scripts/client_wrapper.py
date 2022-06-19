from binance.client import Client
from requests.exceptions import ConnectionError
from time import sleep
from threading import Lock
from config import API_KEY, API_SECRET

# global Variables
client = Client(API_KEY, API_SECRET)

# for accessing client
client_lock = Lock()

# wrapper to keep retrying api calls, while we get connection errors
def retry_conn(func, **kwargs):
   # trying 10 times to connect
   count = 10
   sleep(0.25)
   while count > 0:
      try:
         # try to get a response with the lock
         with client_lock:
            res = func(**kwargs)
            return res
      except ConnectionError as e:
         sleep(0.5)
         count -= 1
         if count == 0:
            # 10 retries failed, throws exception
            print(f"Connection failed, {count} tries failed: no retry")
            raise RuntimeError("10 retries failed") from e
 

# warp the different functions
def futures_account_balance(**kw):
   return retry_conn(client.futures_account_balance, **kw)


def futures_position_information(**kw):
   return retry_conn(client.futures_position_information, **kw)


def futures_klines(**kw):
   return retry_conn(client.futures_klines, **kw)


def futures_create_order(**kw):
   return retry_conn(client.futures_create_order, **kw)


def futures_change_leverage(**kw):
   return retry_conn(client.futures_change_leverage, **kw)


def futures_get_open_orders(**kw):
   return retry_conn(client.futures_get_open_orders, **kw)


def futures_get_order(**kw):
   return retry_conn(client.futures_get_order, **kw)


def futures_cancel_all_open_orders(**kw):
   return retry_conn(client.futures_cancel_all_open_orders, **kw)


def futures_change_margin_type(**kw):
   return retry_conn(client.futures_change_margin_type, **kw)


def futures_symbol_ticker(**kw):
   return retry_conn(client.futures_symbol_ticker, **kw)


def futures_top_longshort_position_ratio(**kw):
   return retry_conn(client.futures_top_longshort_position_ratio, **kw)


def futures_account(**kw):
   return retry_conn(client.futures_account, **kw)
