# API Keys for the Binance API (Make sure that Futures trading is enabled.)
API_KEY = ''
API_SECRET = ''
# Crypto Currency Pair to trade.
COIN = 'BTC'
BASE = 'BUSD'
SYMBOL = COIN + BASE
# Trading amount (in the traded currency, here BTC).
TRADING_AMT = 0.01
# Leverage to use for the trades.
LEVERAGE = 1
# Time frame to look at for the "Top Trader Long/Short Ratio(Positions)".
TIME_FRAME = '1h'
# Reaction time of the bot in seconds. (How long to wait between each check of the ratio.)
REACTION_TIME = 300
# Telegram Bot Token and Chat ID. Updates are sent to this chat in addition to just being logged/printed. [OPTIONAL]
TOKEN = ''
CHAT_ID = ''
