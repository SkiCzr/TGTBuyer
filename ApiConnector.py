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
    try:
        tickers = session.get_tickers(
            category="spot",
            symbol=pair,
        )
    except InvalidRequestError as e:
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
    coin_list1 = session.get_instruments_info(
        category="linear",
    )['result']['list']
    for coin in coin_list:
        if len(coin['baseCoin']) > 1:
            coins.append(coin['baseCoin'])
    for coin in coin_list1:
        if len(coin['baseCoin']) > 1:
            coins.append(coin['baseCoin'])
    return set(coins)

def get_position_info(session, trade):
    response = session.get_positions(
        category="linear",
        symbol=trade.pair,
    )
    return response

def run_updater(session, group, trade):
    hit_checkpoints = []
    print(f"Updater for {trade.pair} is running")
    try:
        while len(hit_checkpoints) != len(group.checkpoints):
            position_info = get_position_info(session, trade)
            current_roi = position_info['result']['list'][0]['unrealisedPnl']
            roi_percentage = float(current_roi)/(trade.entrySum/25) * 100
            for key, value in group.checkpoints.items():
                if key not in hit_checkpoints:

                    if 0 > float(key) > roi_percentage:
                        trade.calcCustomBounds(float(value[0]) / 100, float(value[1]) / 100)
                        set_tp_sl(session, trade.pair, trade.take_profit_custom, trade.stop_loss_custom)
                        hit_checkpoints.append(key)
                        print(f"Hit checkpoint at {key} and changed tp to {trade.take_profit_custom} and sl to {trade.stop_loss_custom}")

                    elif 0 < float(key) < roi_percentage:
                        trade.calcCustomBounds(float(value[0]) / 100, float(value[1]) / 100)
                        set_tp_sl(session, trade.pair, trade.take_profit_custom, trade.stop_loss_custom)
                        hit_checkpoints.append(key)
                        print(f"Hit checkpoint at {key} and changed tp to {trade.take_profit_custom} and sl to {trade.stop_loss_custom}")
    except ValueError as e:
        print(f"Trade on {trade.pair} closed")


def set_tp_sl(session, pair, tp, sl):
    session.set_trading_stop(
        category="linear",
        symbol=pair,
        takeProfit=round(tp, 5),
        stopLoss=round(sl, 5),
        tpTriggerBy="MarkPrice",  # Use MarkPrice to trigger TP
        slTriggerBy="MarkPrice",  # Use MarkPrice to trigger SL
        tpslMode="Full",  # Apply both TP and SL
        positionIdx=0  # Apply for both long and short positions
    )

def open_position(session, trade):

    current_price = float(get_current_price(session, trade.pair))
    quantity = int(trade.entrySum / current_price)
    try:
        set_leverage(session, trade.pair, trade.leverage)
    except InvalidRequestError as e:
        print("Leverage not changed")
    if trade.trade_type == "SHORT":
        side = "Sell"
    else:
        side = "Buy"
    print("Quantity:", quantity)
    place_order_response = session.place_order(
        category="linear",
        symbol=trade.pair,
        side=side,
        orderType="Market",
        qty=str(quantity),
        orderFilter="Order",
    )
    print(place_order_response)
    set_tp_sl(session, trade.pair, trade.take_profit_custom, trade.stop_loss_custom)