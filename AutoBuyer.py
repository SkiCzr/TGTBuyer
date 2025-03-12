import copy
import json
import os
from tkinter import messagebox

from GroupParams import GroupParams
from TGReader import run_telegram_listener

def get_credentials():
    credentials = {
        "telegram_api_key": input("Enter Telegram API Key: "),
        "telegram_api_hash": input("Enter Telegram API Hash: "),
        "bybit_api_key": input("Enter Bybit API Key: "),
        "bybit_api_secret": input("Enter Bybit API Secret: ")
    }
    return credentials


def get_groups():
    groups = []
    num_groups = int(input("How many groups do you want to add? "))

    for i in range(num_groups):
        print(f"\nEntering details  for group {i + 1}:")
        group = {
            "name": input("Group name: "),
            "balance_percentage": float(input("Balance percentage: ")),
            "trade_leverage": float(input("Trading leverage: ")),
            "initial_tp": float(input("Initial Take Profit (TP): ")),
            "initial_sl": float(input("Initial Stop Loss (SL): ")),
            "margin_type": input("Margin Type (cross/isolated): ").lower(),
            "checkpoints": []
        }

        num_checkpoints = int(input("How many checkpoints for this group? "))

        for j in range(num_checkpoints):
            print(f"  Entering details for checkpoint {j + 1}:")
            checkpoint = {
                "mark": float(input("    Mark (percentage): ")),
                "new_tp": float(input("    New TP: ")),
                "new_sl": float(input("    New SL: ")),
                "sell_percentage": float(input("    Sell percentage from position: "))
            }
            group["checkpoints"].append(checkpoint)

        groups.append(group)

    return groups

def save_to_json(data, filename="parameters.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_from_file(filename="parameters.json"):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def run_listener(listener_params):
    print("Telegram API Key:", listener_params['credentials']['telegram_api_key'])
    print("Telegram API Hash:", listener_params['credentials']['telegram_api_hash'])
    print("Bybit API Key:", listener_params['credentials']['bybit_api_key'])
    print("Bybit API Secret:", listener_params['credentials']['bybit_api_secret'])

    telegram_api_key = listener_params['credentials']['telegram_api_key']
    telegram_api_hash = listener_params['credentials']['telegram_api_hash']
    bybit_api_key = listener_params['credentials']['bybit_api_key']
    bybit_api_secret = listener_params['credentials']['bybit_api_secret']
    groups = {}

    for group in listener_params['groups']:
        checkpoint_data = {}
        group_name = group['name']
        balance = group['balance_percentage']
        leverage = group['trade_leverage']
        take_profit = group['initial_tp']
        stop_loss = group['initial_sl']
        margin_type = group['margin_type']
        print(f"Name: {group_name}")
        # Check for associated checkpoints

        for cp in group['checkpoints']:
            print(cp['mark'], cp['new_tp'], cp['new_sl'], cp['sell_percentage'])
            checkpoint_data[cp['mark']] = (cp['new_tp'], cp['new_sl'], cp['sell_percentage'])

        groups[group_name] = GroupParams(group_name, balance, leverage, take_profit, stop_loss, margin_type,
                                  copy.deepcopy(checkpoint_data))

    run_telegram_listener(telegram_api_key, telegram_api_hash, bybit_api_key, bybit_api_secret, groups)

def newStart():
    listener_params = {
        "credentials": get_credentials(),
        "groups": get_groups()
    }
    save_to_json(listener_params)
    print("\nData saved to params.json successfully!")
    return listener_params



if  not os.path.exists('parameters.json') or os.stat('parameters.json').st_size == 0:
    print('Running new confing function')
    data = newStart()
else:
    try:
        data = read_from_file()
    except Exception as e:
        print(e)
        messagebox.showinfo("Failed", "Something is wrong with the file")
run_listener(data)