from ApiConnector import get_max_leverage, open_session, get_current_price, get_wallet_balance, open_position, \
    get_risk_limit
from Trade import MyTrade

balance_percentage = float(10)
session = open_session("32fcMdMPVeuJJLliGM", "apC8QGH2jllfotbJDOc55m3cBULbKrT19wZb")
trade = MyTrade("LONG", "IMXUSDT")
wallet_balance = get_wallet_balance(session, 'USDT')
max_leverage = float(get_max_leverage(session, trade.pair))

risk_limit =get_risk_limit(session, trade.pair)

if 120 > max_leverage:
    trade.leverage = max_leverage
else:
    trade.leverage = 120
print(max_leverage, trade.leverage)
print(trade.leverage)
entryPoint = float(get_current_price(session, trade.pair))
suma = wallet_balance * (balance_percentage / 100) * trade.leverage
if suma >= risk_limit:
    suma = risk_limit - (0.05 * risk_limit)
print(suma)
trade.enterPosition(entryPoint, suma)
tp = float(40)
sl = float(-50)
trade.calcCustomBounds(tp / 100, sl / 100)
group = {}
open_position(session, trade, group)