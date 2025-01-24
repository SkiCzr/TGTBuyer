from ApiConnector import open_session
from Decomposers import MessageDecomposer

API_KEY = "32fcMdMPVeuJJLliGM"
API_SECRET = "apC8QGH2jllfotbJDOc55m3cBULbKrT19wZb"
session = open_session(API_KEY, API_SECRET)
trade = MessageDecomposer(session, 'xrpenis soliriuana :SHORT RENDERAN BTC LONGER')
print(trade.trade_type)
print(trade.pair)
