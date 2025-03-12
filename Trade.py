import json
import os
from datetime import datetime
import re

import pytz


class MyTrade:
    def __init__(self, trade_type, pair):
        self.trade_type = trade_type
        self.pair = pair
        self.leverage = 0
        self.entryPrice = 0
        self.quantity = 0
        self.take_profit1 = 0
        self.take_profit2 = 0
        self.take_profit3 = 0
        self.take_profit4 = 0
        self.take_profit5 = 0
        self.take_profit6 = 0
        self.take_profit_custom = 0
        self.stop_loss1 = 0
        self.stop_loss2 = 0
        self.stop_loss_custom = 0
        self.entrySum = 0


    #Function that calcualtes the stop losses and take profits based on entryPoint
    def enterPosition(self, entryPrice, entrySum):
        self.entryPrice = entryPrice
        self.entrySum = entrySum
        self.quantity = entrySum/entryPrice
        multiplier = 1 if self.trade_type == 'LONG' else -1

        self.take_profit1 = self.calcBound(multiplier * 0.10)
        self.take_profit2 = self.calcBound(multiplier * 0.20)
        self.take_profit3 = self.calcBound(multiplier * 0.25)
        self.take_profit4 = self.calcBound(multiplier * 0.30)
        self.take_profit5 = self.calcBound(multiplier * 0.40)
        self.take_profit6 = self.calcBound(multiplier * 0.50)
        self.stop_loss1 = self.calcBound(multiplier * -0.2)
        self.stop_loss2 = self.calcBound(multiplier * -0.3)

    def calcCustomBounds(self, take_profit_percentage, stop_loss_percentage):
        multiplier = 1 if self.trade_type == 'LONG' else -1
        self.take_profit_custom = self.calcBound(multiplier * take_profit_percentage)
        self.stop_loss_custom = self.calcBound(multiplier * stop_loss_percentage)

    def calcBound(self, percentage):
        return self.entryPrice * (1 + (percentage / self.leverage))

    def calculate_profit(self, entry: float, exit: float):
        self.entryPrice = entry
        print("Entry:",entry)
        print("Exit:", exit)

        if self.trade_type == "LONG":
            percent_change = ((exit - entry) / entry) * 100
        elif self.trade_type == "SHORT":
            percent_change = ((entry - exit) / entry) * 100
        else:
            raise ValueError("Invalid position type. Use 'LONG' or 'SHORT'.")

        return round(percent_change * self.leverage, 5)


    def save_trade(self, group, profit, folder="TradingStats"):

        amsterdam_tz = pytz.timezone('Europe/Amsterdam')

        # Ensure the folder exists
        os.makedirs(folder, exist_ok=True)
        current_time = datetime.now(amsterdam_tz).strftime('%d-%m-%Y %H:%M:%S')
        entryPoint = self.entryPrice
        timestamp = datetime.now()
        # Define file path inside the folder
        clean_name = re.sub(r'[<>:"/\\|?*]', "_", group.name)
        filename = os.path.join(folder, f"{clean_name}.json")

        # Check if the file exists and read existing data
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {"trades": [], "overall_profit%": 0}
        else:
            data = {"trades": [], "overall_profit%": 0}

        # Update overall profit
        data["overall_profit%"] += profit

        # Add new trade
        trade_data = {
            "pair": self.pair,
            "entryPrice": entryPoint,
            "profit%": profit,
            "timestamp": current_time
        }
        data["trades"].append(trade_data)

        # Save back to the file
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Trade saved in {filename}. Overall profit: {data['overall_profit%']:.2f}%")