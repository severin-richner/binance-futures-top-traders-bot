# API Keys for the Binance API (Make sure that Futures trading is enabled.)
API_KEY = ''
API_SECRET = ''
# Crypto Currency Pairs to trade. (make sure they are in lists, here BTCBUSD and ETHUSDT)
COINS = ['BTC', 'ETH']
BASES = ['BUSD', 'USDT']
SYMBOLS = list(zip(COINS, BASES))
# Trading amounts (in the traded currency, here BTC, ETH).
TRADING_AMTS = [0.01, 0.1]
# Leverage to use for the trades. Same index as lists above.
LEVERAGES = [1, 1]
# Time frame to look at for the "Top Trader Long/Short Ratio(Positions)". Same index as lists above.
TIME_FRAME = ['1h', '4h']
# Reaction time of the bot in seconds. (How long to wait between each check of the ratio.) Same index as lists above.
REACTION_TIME = [300, 600]
# Telegram Bot Token and Chat ID. Updates are sent to this chat in addition to just being logged/printed. [OPTIONAL]
TOKEN = ''
CHAT_ID = ''
# If GUI Dashboard should be run or not.
DASHBOARD = False