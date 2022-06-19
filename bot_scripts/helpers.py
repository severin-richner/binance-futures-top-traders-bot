from datetime import datetime
from datetime import time as dtime
import bot_scripts.client_wrapper as cw
import json
from time import sleep
import logging
import bot_scripts.request_wrapper as rw
import bot_scripts.futures_info as futures_info
from config import TOKEN, CHAT_ID

# logging
logging.basicConfig(filename=f'Trading_Bot_Log.log', level=logging.INFO)


def timeNow():
    """ current timestamp """
    return datetime.now().strftime("%H:%M:%S")


def next_status_time():
    """ returns time in the format HH:MM:SS for the next status time (always in 15 min intervals) """
    now = datetime.now()
    h = now.hour
    m = now.minute
    if 0 <= m < 15:
        m = 15
    elif 15 <= m < 30:
        m = 30
    elif 30 <= m < 45:
        m = 45
    elif 45 <= m < 60:
        m = 0
        h = (h + 1) % 24
    return dtime(hour=h, minute=m, second=0).strftime("%H:%M:%S")


def futures_balance(base):
    """ amount for base-currency in futures account """
    balances = cw.futures_account_balance()

    for b in balances:
        if b['asset'] == base:
            return float(b['balance'])


def futures_available(base):
    """ amount for available base currency (now USDT) in futures account """
    balances = cw.futures_account_balance()

    for b in balances:
        if b['asset'] == base:
            return float(b['withdrawAvailable'])


def telegram_msg(msg):
    """ sends telegram message """
    if TOKEN != '' and CHAT_ID != '':
        rw.request(method='GET', timeout=0.5, url='https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '+&text=' + str(msg))
    return


def status(additional):
    """ prints status, logs it and sends it per telegram (if token is given) message
        additonal:      optional string as additional information  """
   
    status_msg = f"{timeNow()} " + additional
    print(status_msg)
    logging.info(status_msg)
    telegram_msg(status_msg)
    return


def current_position_amount(symbol):
    """ returns position amount for current BTC position """
    position_info = cw.futures_position_information(symbol=symbol)[0]               # get position info
    return float(position_info['positionAmt'])                                      # neg for short, pos for long


def refresh_info():
    """ refreshes the futures_info.py file """
    print("Refreshing futures info...")
    with open("./bot_scripts/futures_info.py", "w") as file:
        today = datetime.today()
        current_date = today.strftime("%d.%m.%Y")
        file.write(f"\"\"\"\nbinance exchange info, last updated {current_date}\n(Used as lookup table for \"quantityPrecision\" and \"pricePrecision\" of coins.)\n\"\"\"\ninfo = ")
         
    info = cw.client.futures_exchange_info()
    with open("./bot_scripts/futures_info.py", "a") as file:
        content = json.dumps(info)
        content = content.replace('true', 'True')
        content = content.replace('false', 'False')
        file.write(content)
    return


def get_quantity_precision(symbol):
    for x in futures_info.info['symbols']:
        if x['symbol'] == symbol:
            return int(x['quantityPrecision'])
    return -1


def get_price_precision(symbol):
    for x in futures_info.info['symbols']:
        if x['symbol'] == symbol:
            return int(x['pricePrecision'])
    return -1


def try_market(sym, buy_sell, pos_amount):
    """ market trade to enter trades, side is 'BUY' for long or 'SELL' for short, returns the executed price """

    qty_precision = get_quantity_precision(sym)
    if qty_precision == -1:
        print(msg=f"Quantity precision for {sym} not found!")
        logging.info(msg=f"Quantity precision for {sym} not found!")
        return -1

    qty = round(pos_amount, qty_precision)
    if qty == 0:
        too_little = f"Too little trading_amount to trade {sym}!"
        print(too_little)
        logging.info(msg=too_little)
        telegram_msg(msg=too_little)
        return -1

    try:
        order = cw.futures_create_order(symbol=sym, side=buy_sell, type='MARKET', quantity=round(pos_amount, qty_precision))
    except Exception as e:
        print(e)
        logging.info(msg=str(e))
        telegram_msg(msg=str(e))
        return -1

    o_id = order['orderId']
    while True:
        try:
            stat = (cw.futures_get_order(symbol=sym, orderId=str(o_id)))['status']
            break
        except:
            print('trying to get (market order)')
            logging.info(msg='trying to get (market order)')
            sleep(2)
    while stat != 'FILLED':
        if stat == 'CANCELED':
            print('order was cancelled by user')
            logging.info(msg='order was cancelled by user')
            return -1
        elif stat == 'PENDING_CANCEL':
            print('order is currently unused')
            logging.info(msg='order is currently unused')
        elif stat == 'REJECTED':
            print('order was rejected')
            logging.info(msg='order was rejected')
            return -1
        elif stat == 'EXPIRED':
            print('order expired')
            logging.info(msg='order expired')
            return -1
        sleep(5)
        while True:
            try:
                stat = (cw.futures_get_order(symbol=sym, orderId=str(o_id)))['status']
                break
            except:
                print('trying to get status (market order)')
                logging.info(msg='trying to get status (market order)')
                sleep(2)

    executed_price = float(cw.futures_get_order(symbol=sym, orderId=str(o_id))['avgPrice'])
    # print(f"executed market trade price: {executed_price}")
    return executed_price
