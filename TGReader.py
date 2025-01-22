
import re
from telethon import TelegramClient, events

from ApiConnector import open_session, open_position, get_current_price, get_wallet_balance
from Trade import MyTrade


def DecomposeMessage(message):
    trade_type = re.search(r"LONG|SHORT", message)
    # Checking if the message is a TradeExamples
    if trade_type is None:
        return None
    # Finding info about the TradeExamples by pattern matching
    trade_type = re.search(r"LONG|SHORT", message).group(0)
    pair = re.search(r"\s*([\w\s]+)\s*USDT", message).group(1).strip().replace(" ", "") + "USDT"
    return MyTrade(trade_type, pair, 25)

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
            trade_type = re.search(r"LONG|SHORT", event.text)

            # Checking if the message is a Trade Example
            if trade_type is None:
                return None
            message_text = event.text
            trade = DecomposeMessage(message_text)
            print(trade.pair)
            try:
                entryPoint = float(get_current_price(session, trade.pair))
                trade.enterPosition(entryPoint)
                suma = wallet_balance * (balance_percentage / 100)
                open_position(session, suma, trade)
            except IndexError as e:
                print('This coin does not exist on ByBit futures')
            print(f"New message from {source_group_name}")

    async def main():
        await client.start()
        print("Client started listening for messages...")

    # Run the Telegram client
    client.loop.run_until_complete(main())
    client.run_until_disconnected()


