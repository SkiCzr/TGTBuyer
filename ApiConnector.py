import time
import hashlib
import hmac
import requests
from pybit.exceptions import InvalidRequestError
from pybit.unified_trading import HTTP

# Telegram information for message reading
# api_id = '29823304'
# api_hash = 'd86272c7a21d1901be5b2d9b29233028'
# Cezar API key and secret
# API_KEY = "32fcMdMPVeuJJLliGM"
# API_SECRET = "apC8QGH2jllfotbJDOc55m3cBULbKrT19wZb"

# Vlad API key and secret
# API_KEY = "MWXxy4WsdtdfPX4z22"
# API_SECRET = "auZ8y7DgBw6opDtXnWHnkSJXWBuQNKFnUJHB"

def get_current_price(session, pair):
    tickers = session.get_tickers(
        category="linear",
        symbol=pair,
    )
    return tickers["result"]["list"][0]["lastPrice"]
def get_wallet_balance(session, coin):
    print(session.get_wallet_balance(
        accountType="UNIFIED",
        coin=coin,
    ))
    return float(session.get_wallet_balance(
        accountType="UNIFIED",
        coin=coin,
    )['result']['list'][0]['coin'][0]['walletBalance'])
def open_session(API_KEY, API_SECRET):
    session = HTTP(
        demo=True,
        api_key=API_KEY,
        api_secret=API_SECRET,
    )
    return session

def set_leverage(session, pair, leverage):
    print(session.set_leverage(
        category="linear",
        symbol=pair,
        buyLeverage=str(leverage),
        sellLeverage=str(leverage),
    ))

def get_all_coins(session):
    coins = []
    coin_list = session.get_instruments_info(
        category="spot",
    )['result']['list']
    for coin in coin_list:
        if len(coin['baseCoin']) > 1:
            coins.append(coin['baseCoin'])
    return set(coins)

def open_position(session, suma, trade):

    current_price = float(get_current_price(session, trade.pair))
    quantity = int(suma / current_price)
    try:
        set_leverage(session, trade.pair, trade.leverage)
    except InvalidRequestError as e:
        print("Leverage not changed")
    if trade.trade_type == "SHORT":
        side = "Sell"
    else:
        side = "Buy"
    place_order_response = session.place_order(
        category="linear",
        symbol=trade.pair,
        side=side,
        orderType="Market",
        qty=quantity,
        orderFilter="Order",
    )
    print(trade.take_profit_custom, trade.stop_loss_custom)
    print(place_order_response)
    print(session.set_trading_stop(
        category="linear",
        symbol=trade.pair,
        takeProfit=round(trade.take_profit_custom, 5),
        stopLoss=round(trade.stop_loss_custom, 5),
        tpTriggerBy="MarkPrice",  # Use MarkPrice to trigger TP
        slTriggerBy="MarkPrice",  # Use MarkPrice to trigger SL
        tpslMode="Full",  # Apply both TP and SL
        positionIdx=0  # Apply for both long and short positions
    ))