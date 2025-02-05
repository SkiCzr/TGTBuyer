class GroupParams:
    def __init__(self, name, initialParams, checkpoints):
        self.name = name
        self.balancePercentage = initialParams[0]
        self.initialTakeProfit = initialParams[1]
        self.initialStopLoss = initialParams[2]
        self.checkpoints = checkpoints

    def write(self):
        print("Group name:", self.name)
        print("Balance percentage:", self.balancePercentage)
        print("Initial TP:", self.initialTakeProfit)
        print("Initial SL:", self.initialStopLoss)
        print("Number of checkpoints:", len(self.checkpoints))
        for key, value in self.checkpoints.items():
            print(f"When hit {key} % change TP to {value[0]} and SL to {value[1]}")


