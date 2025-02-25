class GroupParams:
    def __init__(self, name, balance_percentage, trade_leverage, initial_tp, initial_sl, margin_type, checkpoints):
        self.name = name
        self.balancePercentage = balance_percentage
        self.tradeLeverage = trade_leverage
        self.initialTakeProfit = initial_tp
        self.initialStopLoss = initial_sl
        self.marginType = margin_type
        self.checkpoints = checkpoints

    def write(self):
        print("Group name:", self.name)
        print("Balance percentage:", self.balancePercentage)
        print("Trading leverage:", self.tradeLeverage)
        print("Initial TP:", self.initialTakeProfit)
        print("Initial SL:", self.initialStopLoss)
        print("Margin type:", self.marginType)
        print("Number of checkpoints:", len(self.checkpoints))
        for key, value in self.checkpoints.items():
            print(f"When hit {key} % change TP to {value[0]} and SL to {value[1]} and sell {value[2]} of the position")

