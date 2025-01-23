import re

from ApiConnector import get_all_coins
from Trade import MyTrade


def MessageDecomposer(session,message):
    trade_type = re.search(r"LONG|SHORT", message)
    # Checking if the message is a TradeExamples
    if trade_type is None:
        return None
    #Finding info about the TradeExamples by pattern matching
    trade_type = re.search(r"LONG|SHORT", message).group(0)
    coins = get_all_coins(session)
    foundCoin = '0'
    for coin in coins:
        if coin != 'USDT':
            if coin in message:
                if foundCoin == '0':
                    foundCoin = coin
                else:
                    if len(foundCoin) < len(coin):
                        foundCoin = coin

    if foundCoin == '0':
        return None
    else:
        pair = foundCoin+'USDT'

    # Returning the newly created MyTrade object from the info in the message
    return MyTrade(trade_type, pair, 25)