
import re
from datetime import datetime

from telethon import TelegramClient, events
import pytz
from ApiConnector import open_session, open_position, get_current_price, get_wallet_balance
from Decomposers import MessageDecomposer
from Trade import MyTrade

# Function to create and run a Telegram client that listens to messages
def run_telegram_listener(api_id, api_hash, bybit_api_key, bybit_api_secret, groups, params):
    run_time = datetime.now(pytz.utc)
    client = TelegramClient("SESH", int(api_id), api_hash)
    session = open_session(bybit_api_key, bybit_api_secret)
    wallet_balance = get_wallet_balance(session, 'USDT')
    @client.on(events.NewMessage)
    async def handler(event):
        """Handle new messages from the source group."""
        chat = await event.get_chat()
        if chat.title in groups:
            print(f"New message from {chat.title}")
            message_text = event.text
            message_text = message_text.replace("*", "")
            print(event)
            trade = MessageDecomposer(session, message_text)
            if trade is not None and event.message.date > run_time:
                try:
                    entryPoint = float(get_current_price(session, trade.pair))
                    trade.enterPosition(entryPoint)
                    balance_percentage = float(params[groups.index(chat.title)][0])
                    tp = float(params[groups.index(chat.title)][1])
                    sl = float(params[groups.index(chat.title)][2])
                    suma = wallet_balance * (balance_percentage / 100)
                    trade.calcCustomBounds(tp / 100, sl / 100)
                    open_position(session, suma, trade)
                except IndexError as e:
                    print('This coin does not exist on ByBit futures')


    async def main():
        await client.start()
        print("Client started listening for messages...")

    # Run the Telegram client
    client.loop.run_until_complete(main())
    client.run_until_disconnected()


