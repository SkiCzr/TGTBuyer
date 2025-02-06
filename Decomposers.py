import re

from ApiConnector import get_all_coins
from Trade import MyTrade


def MessageDecomposer(session,message):
    message = message.upper()
    trade_type = re.search(r"LONG|SHORT", message)
    # Checking if the message is a TradeExamples
    if trade_type is None:
        return None
    #Finding info about the TradeExamples by pattern matching
    try:
        trade_type = re.search(fr"(?<!\w)(SHORT|LONG|ЛОНГ|ШОРТ)(?!\w)", message).group(0)
    except AttributeError as e:
        print('Type of position not defined')
    coins = get_all_coins(session)
    foundCoin = '0'
    if trade_type == "ШОРТ":
        trade_type = "SHORT"
    if trade_type == "ЛОНГ":
        trade_type = "LONG"
    for coin in coins:
        if coin != 'USDT' and coin not in 'SHORT' and coin not in 'LONG':
            if coin in message:

                pattern = fr'(?<![\w.]){coin}(?![\w.])'
                pattern1 = fr'(?<![\w.]){coin}USDT(?![\w.])'
                if re.search(pattern, message) or re.search(pattern1, message):
                    print(coin)
                    foundCoin = coin

    if foundCoin == '0':
        return None
    else:
        pair = foundCoin+'USDT'

    # Returning the newly created MyTrade object from the info in the message
    return MyTrade(trade_type, pair, 25)