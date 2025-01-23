
import re
from telethon import TelegramClient, events

from ApiConnector import open_session, open_position, get_current_price, get_wallet_balance
from Decomposers import MessageDecomposer
from Trade import MyTrade

# Function to create and run a Telegram client that listens to messages
def run_telegram_listener(api_id, api_hash, bybit_api_key, bybit_api_secret, balance_percentage, source_group_name):
    client = TelegramClient("SESH", int(api_id), api_hash)
    session = open_session(bybit_api_key, bybit_api_secret)
    wallet_balance = get_wallet_balance(session, 'USDT')
    @client.on(events.NewMessage)
    async def handler(event):
        """Handle new messages from the source group."""
        chat = await event.get_chat()
        if chat.title == source_group_name:
            print(f"New message from {source_group_name}")
            message_text = event.text
            trade = MessageDecomposer(session, message_text)
            if trade is not None:
                try:
                    entryPoint = float(get_current_price(session, trade.pair))
                    trade.enterPosition(entryPoint)
                    suma = wallet_balance * (balance_percentage / 100)
                    open_position(session, suma, trade)
                except IndexError as e:
                    print('This coin does not exist on ByBit futures')


    async def main():
        await client.start()
        print("Client started listening for messages...")

    # Run the Telegram client
    client.loop.run_until_complete(main())
    client.run_until_disconnected()


