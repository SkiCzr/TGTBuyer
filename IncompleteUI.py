# import copy
# import os
# import tkinter as tk
# from tkinter import messagebox
#
# from FileAutoBuyer import start_from_file, write_to_file
# from GroupParams import GroupParams
# from TGReader import run_telegram_listener
#
# # Store group and checkpoint rows
# dynamic_rows = []
# checkpoints = {}
#
# # Function to get the correct row index
# def get_next_row():
#     row = 6  # Starting row for the first group
#     for group in dynamic_rows:
#         row += 1  # Account for the group row
#         if group[1] in checkpoints:
#             row += len(checkpoints[group[1]])  # Add space for each checkpoint
#     return row
#
# # Function to dynamically add a new group row
# def add_row():
#     row = get_next_row()  # Determine the correct row to place the new group
#
#     # Group Name Label and Entry
#     group_name_label = tk.Label(root, text="Group Name:")
#     group_name_label.grid(row=row, column=0, pady=5, padx=10, sticky="w")
#     group_name_entry = tk.Entry(root, width=20)
#     group_name_entry.grid(row=row, column=1, pady=5, padx=10)
#
#     # Balance Percentage Label and Spinbox
#     balance_label = tk.Label(root, text="Balance %:")
#     balance_label.grid(row=row, column=2, pady=5, padx=10, sticky="w")
#     balance_counter = tk.Spinbox(root, from_=0, to=100, width=5)
#     balance_counter.grid(row=row, column=3, pady=5, padx=10)
#
#     # Take Profit Percentage Label and Spinbox
#     take_profit_label = tk.Label(root, text="Take Profit %:")
#     take_profit_label.grid(row=row, column=4, pady=5, padx=10, sticky="w")
#     take_profit_counter = tk.Spinbox(root, from_=0, to=100, width=5)
#     take_profit_counter.grid(row=row, column=5, pady=5, padx=10)
#
#     # Stop Loss Percentage Label and Spinbox
#     stop_loss_label = tk.Label(root, text="Stop Loss %:")
#     stop_loss_label.grid(row=row, column=6, pady=5, padx=10, sticky="w")
#     stop_loss_counter = tk.Spinbox(root, from_=0, to=100, width=5)
#     stop_loss_counter.grid(row=row, column=7, pady=5, padx=10)
#
#     # Function to remove the group row and its checkpoints
#     def remove_row():
#         group_elements = [group_name_label, group_name_entry, balance_label, balance_counter,
#                           take_profit_label, take_profit_counter, stop_loss_label, stop_loss_counter,
#                           remove_button, checkpoint_button]
#         for widget in group_elements:
#             widget.destroy()
#
#         # Remove associated checkpoints
#         if group_name_entry in checkpoints:
#             for widgets in checkpoints[group_name_entry]:
#                 for widget in widgets:
#                     widget.destroy()
#             del checkpoints[group_name_entry]
#
#         dynamic_rows.remove(group_elements)
#
#     # Function to add a checkpoint row below the group row
#     def add_checkpoint():
#         checkpoint_row = get_next_row()  # Get the correct position for the checkpoint
#
#         # "When hit" label and number picker
#         when_hit_label = tk.Label(root, text="When hit:")
#         when_hit_label.grid(row=checkpoint_row, column=1, pady=5, padx=10, sticky="w")
#         when_hit_spinbox = tk.Spinbox(root, from_=0, to=100, width=5)
#         when_hit_spinbox.grid(row=checkpoint_row, column=2, pady=5, padx=10)
#
#         # "Change TP to" label and number picker
#         change_tp_label = tk.Label(root, text="Change TP to:")
#         change_tp_label.grid(row=checkpoint_row, column=3, pady=5, padx=10, sticky="w")
#         change_tp_spinbox = tk.Spinbox(root, from_=0, to=100, width=5)
#         change_tp_spinbox.grid(row=checkpoint_row, column=4, pady=5, padx=10)
#
#         # "And SL to" label and number picker
#         change_sl_label = tk.Label(root, text="And SL to:")
#         change_sl_label.grid(row=checkpoint_row, column=5, pady=5, padx=10, sticky="w")
#         change_sl_spinbox = tk.Spinbox(root, from_=0, to=100, width=5)
#         change_sl_spinbox.grid(row=checkpoint_row, column=6, pady=5, padx=10)
#
#         # Remove checkpoint button
#         def remove_checkpoint():
#             for widget in (when_hit_label, when_hit_spinbox, change_tp_label, change_tp_spinbox,
#                            change_sl_label, change_sl_spinbox, remove_cp_button):
#                 widget.destroy()
#             checkpoints[group_name_entry].remove([when_hit_label, when_hit_spinbox, change_tp_label,
#                                                   change_tp_spinbox, change_sl_label, change_sl_spinbox,
#                                                   remove_cp_button])
#
#         remove_cp_button = tk.Button(root, text="Remove checkpoint", command=remove_checkpoint)
#         remove_cp_button.grid(row=checkpoint_row, column=7, pady=5, padx=10)
#
#         # Store checkpoint rows
#         if group_name_entry not in checkpoints:
#             checkpoints[group_name_entry] = []
#         checkpoints[group_name_entry].append([when_hit_label, when_hit_spinbox, change_tp_label,
#                                               change_tp_spinbox, change_sl_label, change_sl_spinbox,
#                                               remove_cp_button])
#
#     # Remove Group Button
#     remove_button = tk.Button(root, text="Remove group", command=remove_row)
#     remove_button.grid(row=row, column=8, pady=5, padx=10)
#
#     # Add Checkpoint Button
#     checkpoint_button = tk.Button(root, text="Add checkpoint", command=add_checkpoint)
#     checkpoint_button.grid(row=row, column=9, pady=5, padx=10)
#
#     dynamic_rows.append([group_name_label, group_name_entry, balance_label, balance_counter,
#                          take_profit_label, take_profit_counter, stop_loss_label, stop_loss_counter,
#                          remove_button, checkpoint_button])
#
#
# # Function to save and start the app
# def save_and_start():
#     api_key = api_key_entry.get()
#     api_secret = api_secret_entry.get()
#     telegram_api_id = telegram_api_id_entry.get()
#     telegram_api_hash = telegram_api_hash_entry.get()
#
#     print("API Key:", api_key)
#     print("API Secret:", api_secret)
#     print("Telegram API ID:", telegram_api_id)
#     print("Telegram API Hash:", telegram_api_hash)
#
#     groups = []
#
#     for group_elements in dynamic_rows:
#         checkpoint_data = {}
#         group_name = group_elements[1].get()
#         balance = int(group_elements[3].get())
#         take_profit = int(group_elements[5].get())
#         stop_loss = int(group_elements[7].get())
#
#
#         # Check for associated checkpoints
#         if group_elements[1] in checkpoints:
#
#             for cp in checkpoints[group_elements[1]]:
#                 print(cp[1].get(), cp[3].get(), cp[5].get())
#                 checkpoint_data[cp[1].get()] = (cp[3].get(), cp[5].get())
#
#         groups.append(GroupParams(group_name, (balance, take_profit, stop_loss), copy.deepcopy(checkpoint_data)))
#
#
#
#     write_to_file(telegram_api_id, telegram_api_hash, api_key, api_secret, groups)
#     root.destroy()
#     run_telegram_listener(telegram_api_id, telegram_api_hash, api_key, api_secret, groups)
#
#
# # Initialize the main application window
# root = tk.Tk()
# root.title("Parameter Configuration")
# root.geometry("1200x600")
#
# # Create and place labels and textboxes for API parameters
# tk.Label(root, text="API Key:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
# api_key_entry = tk.Entry(root, width=30)
# api_key_entry.grid(row=0, column=1, pady=5, padx=10, columnspan=2)
#
# tk.Label(root, text="API Secret:").grid(row=1, column=0, pady=5, padx=10, sticky="w")
# api_secret_entry = tk.Entry(root, width=30, show="*")
# api_secret_entry.grid(row=1, column=1, pady=5, padx=10, columnspan=2)
#
# tk.Label(root, text="Telegram API ID:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
# telegram_api_id_entry = tk.Entry(root, width=30)
# telegram_api_id_entry.grid(row=2, column=1, pady=5, padx=10, columnspan=2)
#
# tk.Label(root, text="Telegram API Hash:").grid(row=3, column=0, pady=5, padx=10, sticky="w")
# telegram_api_hash_entry = tk.Entry(root, width=30)
# telegram_api_hash_entry.grid(row=3, column=1, pady=5, padx=10, columnspan=2)
#
# # Add Group Button
# plus_button = tk.Button(root, text="+ Add Group", command=add_row)
# plus_button.grid(row=5, column=0, columnspan=9, pady=10)
#
# # Add Start Button
# start_button = tk.Button(root, text="Start", command=save_and_start)
# start_button.grid(row=20, column=0, columnspan=9, pady=20)
#
# if  not os.path.exists('params') or os.stat('params').st_size == 0:
#     print('da')
#     root.mainloop()
# else:
#     try:
#         start_from_file()
#     except Exception as e:
#         print(e)
#         messagebox.showinfo("Failed", "Something is wrong with the file")