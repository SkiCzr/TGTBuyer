import tkinter as tk
from tkinter import messagebox

from TGReader import run_telegram_listener


# Function to save input data to variables
def save_and_start():
    group_name = group_name_entry.get()
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    try:
        balance_percentage = int(balance_percentage_counter.get())
        # stop_loss_percentage = int(stop_loss_counter.get())
        # take_profit_percentage = int(take_profit_counter.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Percentage fields must be integers.")
        return

    telegram_api_id = telegram_api_id_entry.get()
    telegram_api_hash = telegram_api_hash_entry.get()

    # Output the variables (can be replaced with any other functionality)
    print("Group Name:", group_name)
    print("API Key:", api_key)
    print("API Secret:", api_secret)
    print("Balance Percentage:", balance_percentage)
    # print("Stop Loss Percentage:", stop_loss_percentage)
    # print("Take Profit Percentage:", take_profit_percentage)
    print("Telegram API ID:", telegram_api_id)
    print("Telegram API Hash:", telegram_api_hash)

    messagebox.showinfo("Success", "Parameters saved successfully and process started!")
    root.destroy()  # Close the window after pressing Start
    run_telegram_listener(telegram_api_id, telegram_api_hash, api_key, api_secret,
                          balance_percentage, group_name)

# Create the main application window
root = tk.Tk()
root.title("Parameter Configuration")
root.geometry("350x400")

# Create and place labels and textboxes
# Group Name
tk.Label(root, text="Group Name:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
group_name_entry = tk.Entry(root, width=30)
group_name_entry.grid(row=0, column=1, pady=5, padx=10)

# API Key
tk.Label(root, text="API Key:").grid(row=1, column=0, pady=5, padx=10, sticky="w")
api_key_entry = tk.Entry(root, width=30)
api_key_entry.grid(row=1, column=1, pady=5, padx=10)

# API Secret
tk.Label(root, text="API Secret:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
api_secret_entry = tk.Entry(root, width=30, show="*")
api_secret_entry.grid(row=2, column=1, pady=5, padx=10)

# Telegram API ID
tk.Label(root, text="Telegram API ID:").grid(row=3, column=0, pady=5, padx=10, sticky="w")
telegram_api_id_entry = tk.Entry(root, width=30)
telegram_api_id_entry.grid(row=3, column=1, pady=5, padx=10)

# Telegram API Hash
tk.Label(root, text="Telegram API Hash:").grid(row=4, column=0, pady=5, padx=10, sticky="w")
telegram_api_hash_entry = tk.Entry(root, width=30)
telegram_api_hash_entry.grid(row=4, column=1, pady=5, padx=10)

# Balance Percentage
balance_percentage_label = tk.Label(root, text="Balance Percentage:")
balance_percentage_label.grid(row=5, column=0, pady=5, padx=10, sticky="w")
balance_percentage_counter = tk.Spinbox(root, from_=0, to=100, width=5)
balance_percentage_counter.grid(row=5, column=1, pady=5, padx=10, sticky="w")

# # Stop Loss Percentage
# tk.Label(root, text="Stop Loss Percentage:").grid(row=6, column=0, pady=5, padx=10, sticky="w")
# stop_loss_counter = tk.Spinbox(root, from_=0, to=100, width=5)
# stop_loss_counter.grid(row=6, column=1, pady=5, padx=10, sticky="w")
#
# # Take Profit Percentage
# tk.Label(root, text="Take Profit Percentage:").grid(row=7, column=0, pady=5, padx=10, sticky="w")
# take_profit_counter = tk.Spinbox(root, from_=0, to=100, width=5)
# take_profit_counter.grid(row=7, column=1, pady=5, padx=10, sticky="w")

# Start Button
start_button = tk.Button(root, text="Start", command=save_and_start)
start_button.grid(row=8, column=0, columnspan=2, pady=20)

# Run the application in the background
root.mainloop()
