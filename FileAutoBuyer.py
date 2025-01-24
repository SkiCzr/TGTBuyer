from tkinter import messagebox

from TGReader import run_telegram_listener


def start_from_file():
    group_names = []
    group_params = []
    with open("params", "r") as file:
        lines = file.readlines()
        try:
            telegram_api_key = lines[0].strip()
            telegram_api_hash = lines[1].strip()
            bybit_api_key = lines[2].strip()
            bybit_api_secret = lines[3].strip()
            for i in range(4, len(lines)):
                group = lines[i].split('###')
                name = group[0]
                balance_percentage = group[1]
                take_profit = group[2]
                stop_loss = group[3]
                group_names.append(name)
                group_params.append((balance_percentage, take_profit, stop_loss))
        except IndexError as e:
            messagebox.showinfo("Failed", "Not enough parameters mentioned")
    print(group_names)
    print(group_params)
    run_telegram_listener(telegram_api_key, telegram_api_hash, bybit_api_key, bybit_api_secret, group_names, group_params)

def write_to_file(telegram_api_key, telegram_api_hash, bybit_api_key, bybit_api_secret, group_names, group_params):
    with open('params', "w") as file:
        file.write(f"{telegram_api_key}\n")
        file.write(f"{telegram_api_hash}\n")
        file.write(f"{bybit_api_key}\n")
        file.write(f"{bybit_api_secret}\n")
        for i in range(0, len(group_names)):
            file.write(f"{group_names[i]}###{group_params[i][0]}###{group_params[i][1]}###{group_params[i][2]}###\n")
        file.close()