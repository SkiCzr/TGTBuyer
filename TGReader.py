import asyncio
import re
from datetime import datetime
from telethon import TelegramClient, events
import pytz
from ApiConnector import open_session, open_position, get_current_price, get_wallet_balance, run_updater, \
    get_max_leverage, get_risk_limit
from Decomposers import MessageDecomposer



# Function to create and run a Telegram client that listens to messages
def run_telegram_listener(api_id, api_hash, bybit_api_key, bybit_api_secret, groups):
    run_time = datetime.now(pytz.utc)
    client = TelegramClient("SESH", int(api_id), api_hash)
    print(api_id, api_hash)
    session = open_session(bybit_api_key, bybit_api_secret)
    wallet_balance = get_wallet_balance(session, 'USDT')
    print("Wallet balance", wallet_balance)
    @client.on(events.NewMessage)
    async def handler(event):
        """Handle new messages from the source group."""
        chat = await event.get_chat()
        try:
            if chat.title in groups:

                message_text = event.text
                message_text = message_text.replace("*", "")
                print(f"[{datetime.now(pytz.utc)}] New message from", chat.title)
                trade = MessageDecomposer(session, message_text)
                if trade is not None and event.message.date > run_time:
                    try:
                        print(f"[{datetime.now(pytz.utc)}] New trade from {chat.title}")
                        group = groups[chat.title]
                        balance_percentage = float(group.balancePercentage)
                        risk_limit = get_risk_limit(session, trade.pair)
                        max_leverage = float(get_max_leverage(session, trade.pair))
                        if group.tradeLeverage > max_leverage:
                            trade.leverage = max_leverage
                        else:
                            trade.leverage = group.tradeLeverage
                        print(max_leverage, trade.leverage)
                        entryPoint = float(get_current_price(session, trade.pair))
                        suma = wallet_balance * (balance_percentage / 100) * trade.leverage
                        if suma >= risk_limit:
                            suma = risk_limit - (0.05 * risk_limit)
                        trade.enterPosition(entryPoint, suma)
                        tp = float(group.initialTakeProfit)
                        sl = float(group.initialStopLoss)
                        trade.calcCustomBounds(tp / 100, sl / 100)

                        open_position(session, trade, group)
                        print(f"{trade.trade_type} position opened on {trade.pair}")
                        await asyncio.to_thread(run_updater, session, group, trade)

                    except IndexError as e:
                        print('This coin does not exist on ByBit futures')
        except AttributeError as e:
            print(f'[{datetime.now(pytz.utc)}] Message from a user')

    async def main():
        await client.start()
        print("Client started listening for messages...")

    # Run the Telegram client
    client.loop.run_until_complete(main())
    client.run_until_disconnected()


