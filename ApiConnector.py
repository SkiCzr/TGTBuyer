import asyncio
import math
import time
import hashlib
import hmac
from decimal import Decimal

import requests
from pybit.exceptions import InvalidRequestError
from pybit.unified_trading import HTTP
from unicodedata import decimal


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

def get_last_closed(session, n):
    return session.get_closed_pnl(
    category="linear",
    limit=n,
    )['result']['list']

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

def get_max_leverage(session, pair):
    return session.get_risk_limit(
            category="linear",
            symbol=pair,
            )['result']['list'][0]['maxLeverage']

def get_risk_limit(session, pair):
    return float(session.get_risk_limit(
            category="linear",
            symbol="IMXUSDT",
            )['result']['list'][0]['riskLimitValue'])


def set_margin_mode(session, pair, leverage, margin_mode):
    print(margin_mode)
    if margin_mode == "cross":
        bin_margin = 0
    else:
        bin_margin = 1

    print(session.switch_margin_mode(
        category="linear",
        symbol=pair,
        tradeMode=bin_margin,
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
    current_roi = 0
    percentage_sum = 0
    remaining_percentage = 100
    print(f"Updater for {trade.pair} is running")
    current_sum = trade.entrySum
    try:
        while len(hit_checkpoints) != len(group.checkpoints) and remaining_percentage > 0:

            position_info = get_position_info(session, trade)
            current_roi = position_info['result']['list'][0]['unrealisedPnl']
            roi_percentage = float(current_roi)/(current_sum/trade.leverage) * 100

            for key, value in group.checkpoints.items():

                if key not in hit_checkpoints:
                    if 0 > float(key) > roi_percentage:
                        trade.calcCustomBounds(float(value[0]) / 100, float(value[1]) / 100)
                        set_tp_sl(session, trade.pair, trade.take_profit_custom, trade.stop_loss_custom)

                        if value[2] != "0":
                            print(f"{value[2]} % of {trade.pair} was sold when price hit {key}")
                            sellPosition(session,trade, float(value[2]) / 100)
                            percentage_sum = percentage_sum + ((float(value[2]) / 100) * float(key))
                            print("Added:", ((float(value[2]) / 100) * float(key)))
                            remaining_percentage = remaining_percentage - float(value[2])
                            current_sum = current_sum - (trade.entrySum * float(value[2]) / 100)


                        hit_checkpoints.append(key)
                        print(f"Hit checkpoint at {key} and changed tp to {trade.take_profit_custom} and sl to {trade.stop_loss_custom}")

                    elif 0 < float(key) < roi_percentage:

                        trade.calcCustomBounds(float(value[0]) / 100, float(value[1]) / 100)
                        set_tp_sl(session, trade.pair, trade.take_profit_custom, trade.stop_loss_custom)

                        if value[2] != "0":
                            print(f"{value[2]} % of {trade.pair} was sold when price hit {key}")
                            sellPosition(session,trade, float(value[2]) / 100)
                            percentage_sum = percentage_sum + ((float(value[2]) / 100) * float(key))
                            print("Added:", ((float(value[2]) / 100) * float(key)))
                            remaining_percentage = remaining_percentage - float(value[2])
                            current_sum = current_sum - (trade.entrySum * float(value[2]) / 100)


                        hit_checkpoints.append(key)
                        print(f"Hit checkpoint at {key} and changed tp to {trade.take_profit_custom} and sl to {trade.stop_loss_custom}")

    except ValueError or ZeroDivisionError as e:
        print(f"Trade on {trade.pair} hit the stop loss at{current_roi}")
        time.sleep(3)
        total_profit = current_roi
        percentage_sum += total_profit * (remaining_percentage/100)
    print(f"Trade on {trade.pair} closed")
    trade.save_trade(group, percentage_sum)



def sellPosition(session, trade, qty_percent):
    if trade.trade_type == "SHORT":
        action = "Buy"
    else:
        action = "Sell"
    sellQty = adjust_qty(session, trade.pair, qty_percent * trade.quantity)
    print(sellQty)
    post_order(session, trade.pair, sellQty, action, "Market", 0)

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

def get_order_limit(session, pair):
    coin_info = session.get_instruments_info(
        category="linear",
        symbol=pair
    )['result']['list']
    return coin_info[0]['lotSizeFilter']['maxMktOrderQty']

def adjust_qty(session, pair, qty):
    coin_info = session.get_instruments_info(
        category="linear",
        symbol=pair
    )['result']['list']
    step_size = Decimal(coin_info[0]['lotSizeFilter']['qtyStep'])
    return math.floor(Decimal(qty) / step_size) * step_size

def post_order(session, pair, qty, side, orderType, price):
    orderCap = int(float(get_order_limit(session, pair)))

    while qty > 0:
        if qty >= orderCap:
            session.place_order(
                category="linear",
                symbol=pair,
                side=side,
                orderType=orderType,
                qty=orderCap,
                price=price,
                orderFilter="Order",
            )
        else:
            session.place_order(
                category="linear",
                symbol=pair,
                side=side,
                orderType=orderType,
                qty=qty,
                price=price,
                orderFilter="Order",
            )
        qty -= orderCap


def open_position(session, trade, group):

    current_price = get_current_price(session, trade.pair)
    quantity = adjust_qty(session, trade.pair, trade.entrySum / float(current_price))
    print(quantity * Decimal(current_price))
    try:
        print(trade.leverage)
        set_leverage(session, trade.pair, trade.leverage)

    except InvalidRequestError as e:
        print("Leverage not changed")

    # try:
    #     set_margin_mode(session, trade.pair, trade.leverage, group.marginType)
    # except InvalidRequestError as e:
    #     print("Margin type not changed")

    if trade.trade_type == "SHORT":
        side = "Sell"
    else:
        side = "Buy"

    post_order(session, trade.pair, quantity, side, "Market", 0)
    set_tp_sl(session, trade.pair, trade.take_profit_custom, trade.stop_loss_custom)
