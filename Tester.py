from ApiConnector import open_session, get_current_price, get_wallet_balance

# Cezar API key and secret
API_KEY = "32fcMdMPVeuJJLliGM"
API_SECRET = "apC8QGH2jllfotbJDOc55m3cBULbKrT19wZb"

session = open_session(API_KEY, API_SECRET)
current_price = get_current_price(session, 'XRPUSDT')
print(current_price)
wallet_balance = get_wallet_balance(session, 'USDT')
print(wallet_balance)
