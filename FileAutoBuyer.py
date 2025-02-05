import copy
import traceback
from tkinter import messagebox

from GroupParams import GroupParams
from TGReader import run_telegram_listener



def start_from_file():
    groups = {}
    with open("params", "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        try:
            telegram_api_key = lines[0].strip()
            telegram_api_hash = lines[1].strip()
            bybit_api_key = lines[2].strip()
            bybit_api_secret = lines[3].strip()
            i = 4
            while i < len(lines):
                if lines[i] == "#####":
                    checkpoints = {}
                    group_name =  lines[i+1]
                    group_init = lines[i+2].split('/')
                    i += 3
                while i < len(lines) and lines[i] != '#####' :
                    temp = lines[i].split('/')
                    checkpoints[temp[0]] = (temp[1], temp[2])
                    i += 1
                groups[group_name] = GroupParams(group_name, (group_init[0], group_init[1], group_init[2]), copy.deepcopy(checkpoints))

            print(telegram_api_key)
            print(telegram_api_hash)
            print(bybit_api_key)
            print(bybit_api_secret)
            for key,value in groups.items():
                value.write()
        except IndexError as e:
            messagebox.showinfo("Failed", f" Error: {traceback.extract_tb(e.__traceback__)} Not enough parameters mentioned")
    run_telegram_listener(telegram_api_key, telegram_api_hash, bybit_api_key, bybit_api_secret, groups)

def write_to_file(telegram_api_key, telegram_api_hash, bybit_api_key, bybit_api_secret, groups):
    with open('params', "w", encoding="utf-8") as file:
        file.write(f"{telegram_api_key}\n")
        file.write(f"{telegram_api_hash}\n")
        file.write(f"{bybit_api_key}\n")
        file.write(f"{bybit_api_secret}\n")
        for group in groups:
            file.write("#####\n")
            file.write(f"{group.name}\n")
            file.write(f"{group.balancePercentage}/{group.initialTakeProfit}/{group.initialStopLoss}/\n")
            for key,value in group.checkpoints.items():
                file.write(f"{key}/{value[0]}/{value[1]}/\n")
        file.close()