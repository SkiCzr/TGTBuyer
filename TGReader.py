import asyncio
import re
from datetime import datetime

from telethon import TelegramClient, events
import pytz
from ApiConnector import open_session, open_position, get_current_price, get_wallet_balance, run_updater
from Decomposers import MessageDecomposer
from Trade import MyTrade

# Function to create and run a Telegram client that listens to messages
def run_telegram_listener(api_id, api_hash, bybit_api_key, bybit_api_secret, groups):
    run_time = datetime.now(pytz.utc)
    client = TelegramClient("SESH", int(api_id), api_hash)
    session = open_session(bybit_api_key, bybit_api_secret)
    wallet_balance = get_wallet_balance(session, 'USDT')
    print("Wallet balance", wallet_balance)
    @client.on(events.NewMessage)
    async def handler(event):
        """Handle new messages from the source group."""
        chat = await event.get_chat()
        try:
            if chat.title in groups:
                print(f"New trade from {chat.title}")
                message_text = event.text
                message_text = message_text.replace("*", "")
                print(event)
                trade = MessageDecomposer(session, message_text)
                if trade is not None and event.message.date > run_time:
                    try:
                        group = groups[chat.title]
                        balance_percentage = float(group.balancePercentage)
                        entryPoint = float(get_current_price(session, trade.pair))
                        suma = wallet_balance * (balance_percentage / 100) * 25
                        trade.enterPosition(entryPoint, suma)
                        tp = float(group.initialTakeProfit)
                        sl = float(group.initialStopLoss)
                        trade.calcCustomBounds(tp / 100, sl / 100)
                        open_position(session, trade)
                        await asyncio.to_thread(run_updater, session, group, trade)
                    except IndexError as e:
                        print('This coin does not exist on ByBit futures')
        except AttributeError as e:
            print('Message from a user')

    async def main():
        await client.start()
        print("Client started listening for messages...")

    # Run the Telegram client
    client.loop.run_until_complete(main())
    client.run_until_disconnected()


