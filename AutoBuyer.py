import os
import tkinter as tk
from tkinter import messagebox

from FileAutoBuyer import start_from_file, write_to_file
from TGReader import run_telegram_listener


# Function to dynamically add a new row
def add_row():
    row = len(dynamic_rows) + 6  # Start from row 6 (below existing fields)

    # Group Name Label and Entry
    group_name_label = tk.Label(root, text="Group Name:")
    group_name_label.grid(row=row, column=0, pady=5, padx=10, sticky="w")
    group_name_entry = tk.Entry(root, width=20)
    group_name_entry.grid(row=row, column=1, pady=5, padx=10)

    # Balance Percentage Label and Spinbox
    balance_label = tk.Label(root, text="Balance %:")
    balance_label.grid(row=row, column=2, pady=5, padx=10, sticky="w")
    balance_counter = tk.Spinbox(root, from_=0, to=100, width=5)
    balance_counter.grid(row=row, column=3, pady=5, padx=10)

    # Take Profit Percentage Label and Spinbox
    take_profit_label = tk.Label(root, text="Take Profit %:")
    take_profit_label.grid(row=row, column=4, pady=5, padx=10, sticky="w")
    take_profit_counter = tk.Spinbox(root, from_=0, to=100, width=5)
    take_profit_counter.grid(row=row, column=5, pady=5, padx=10)

    # Stop Loss Percentage Label and Spinbox
    stop_loss_label = tk.Label(root, text="Stop Loss %:")
    stop_loss_label.grid(row=row, column=6, pady=5, padx=10, sticky="w")
    stop_loss_counter = tk.Spinbox(root, from_=0, to=100, width=5)
    stop_loss_counter.grid(row=row, column=7, pady=5, padx=10)

    # Minus button to remove the row
    def remove_row():
        group_name_label.destroy()
        group_name_entry.destroy()
        balance_label.destroy()
        balance_counter.destroy()
        take_profit_label.destroy()
        take_profit_counter.destroy()
        stop_loss_label.destroy()
        stop_loss_counter.destroy()
        minus_button.destroy()
        dynamic_rows.remove((group_name_label, group_name_entry, balance_label, balance_counter,
                             take_profit_label, take_profit_counter, stop_loss_label, stop_loss_counter, minus_button))

    minus_button = tk.Button(root, text="Remove group", command=remove_row)
    minus_button.grid(row=row, column=8, pady=5, padx=10)

    dynamic_rows.append((group_name_label, group_name_entry, balance_label, balance_counter,
                         take_profit_label, take_profit_counter, stop_loss_label, stop_loss_counter, minus_button))


# Function to save the data and start the application
def save_and_start():
    # Save API details
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    telegram_api_id = telegram_api_id_entry.get()
    telegram_api_hash = telegram_api_hash_entry.get()

    print("API Key:", api_key)
    print("API Secret:", api_secret)
    print("Telegram API ID:", telegram_api_id)
    print("Telegram API Hash:", telegram_api_hash)

    # Save group data
    group_names = []
    group_params = []
    for (_, group_name_entry, _, balance_counter, _, take_profit_counter, _, stop_loss_counter, _) in dynamic_rows:
        group_name = group_name_entry.get()
        balance = int(balance_counter.get())
        take_profit = int(take_profit_counter.get())
        stop_loss = int(stop_loss_counter.get())
        group_names.append(group_name)
        group_params.append((balance, take_profit, stop_loss))

    write_to_file(telegram_api_id, telegram_api_hash, api_key, api_secret, group_names, group_params)
    root.destroy()
    run_telegram_listener(telegram_api_id, telegram_api_hash, api_key, api_secret, group_names, group_params)

    print("Group Names:", group_names)
    print("Group Parameters:", group_params)


# Initialize the main application window
root = tk.Tk()
root.title("Parameter Configuration")
root.geometry("900x600")

# Create and place labels and textboxes for API parameters
tk.Label(root, text="API Key:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
api_key_entry = tk.Entry(root, width=30)
api_key_entry.grid(row=0, column=1, pady=5, padx=10, columnspan=2)

tk.Label(root, text="API Secret:").grid(row=1, column=0, pady=5, padx=10, sticky="w")
api_secret_entry = tk.Entry(root, width=30, show="*")
api_secret_entry.grid(row=1, column=1, pady=5, padx=10, columnspan=2)

tk.Label(root, text="Telegram API ID:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
telegram_api_id_entry = tk.Entry(root, width=30)
telegram_api_id_entry.grid(row=2, column=1, pady=5, padx=10, columnspan=2)

tk.Label(root, text="Telegram API Hash:").grid(row=3, column=0, pady=5, padx=10, sticky="w")
telegram_api_hash_entry = tk.Entry(root, width=30)
telegram_api_hash_entry.grid(row=3, column=1, pady=5, padx=10, columnspan=2)

# Add Plus Button for adding rows
plus_button = tk.Button(root, text="+ Add Group", command=add_row)
plus_button.grid(row=5, column=0, columnspan=9, pady=10)

# Add Start Button
start_button = tk.Button(root, text="Start", command=save_and_start)
start_button.grid(row=20, column=0, columnspan=9, pady=20)

# List to keep track of dynamically added rows
dynamic_rows = []

if  not os.path.exists('params') or os.stat('params').st_size == 0:
    print('da')
    root.mainloop()
else:
    try:
        start_from_file()
    except Exception as e:
        print(e)
        messagebox.showinfo("Failed", "Something is wrong with the file")
