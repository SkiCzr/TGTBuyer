
class MyTrade:
    def __init__(self, trade_type, pair, leverage):
        self.trade_type = trade_type
        self.pair = pair
        self.leverage = leverage
        self.entryPrice = 0
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
        self.Status = False
        self.ProfitsStatus = [False,False,False,False,False,False,False,False]


    #Function that calcualtes the stop losses and take profits based on entryPoint
    def enterPosition(self, entryPrice):
        self.entryPrice = entryPrice
        if self.trade_type == "LONG":
            self.take_profit1 = self.calcTakeProfit(100,0.10)
            self.take_profit2 = self.calcTakeProfit(100,0.20)
            self.take_profit3 = self.calcTakeProfit(100,0.25)
            self.take_profit4 = self.calcTakeProfit(100,0.30)
            self.take_profit5 = self.calcTakeProfit(100,0.40)
            self.take_profit6 = self.calcTakeProfit(100,0.50)
            self.stop_loss1 = self.calcStopLoss(100, 0.2)
            self.stop_loss2 = self.calcStopLoss(100, 0.3)
        if self.trade_type == "SHORT":
            self.take_profit1 = self.calcStopLoss(100, 0.10)
            self.take_profit2 = self.calcStopLoss(100, 0.20)
            self.take_profit3 = self.calcStopLoss(100, 0.25)
            self.take_profit4 = self.calcStopLoss(100, 0.30)
            self.take_profit5 = self.calcStopLoss(100, 0.40)
            self.take_profit6 = self.calcStopLoss(100, 0.50)
            self.stop_loss1 = self.calcTakeProfit(100, 0.2)
            self.stop_loss2 = self.calcTakeProfit(100, 0.3)

    def calcCustomBounds(self, take_profit_percentage, stop_loss_percentage):
        if self.trade_type == 'LONG':
            self.take_profit_custom = self.calcTakeProfit(100, take_profit_percentage)
            self.stop_loss_custom = self.calcStopLoss(100, stop_loss_percentage)
        else:
            self.take_profit_custom = self.calcStopLoss(100, take_profit_percentage)
            self.stop_loss_custom = self.calcTakeProfit(100, stop_loss_percentage)


    def calcTakeProfit(self, sum, percentage):
        # Quantity of coins bought for the entry price
        quantity = (sum * self.leverage) / self.entryPrice
        return (sum * self.leverage + (percentage * sum)) / quantity

    def calcStopLoss(self, sum, percentage):
        # Quantity of coins bought for the entry price
        quantity = (sum * self.leverage) / self.entryPrice
        return (sum * self.leverage - (percentage * sum)) / quantity

    def write_trade_details(self, filename):
        # Open the file in append mode (creates the file if it doesn't exist)
        with open(filename, 'a') as file:
            file.write(f"Trade Type: {self.trade_type}\n")
            file.write(f"Pair: {self.pair}\n")
            file.write(f"Leverage: {self.leverage}\n")
            file.write(f"Entry point: {self.entryPrice}\n")
            file.write(f"Take Profit 1 (10%): {self.take_profit1} was hit {self.ProfitsStatus[0]}\n")
            file.write(f"Take Profit 2 (20%): {self.take_profit2} was hit {self.ProfitsStatus[1]}\n")
            file.write(f"Take Profit 3 (25%): {self.take_profit3} was hit {self.ProfitsStatus[2]}\n")
            file.write(f"Take Profit 4 (30%): {self.take_profit4} was hit {self.ProfitsStatus[3]}\n")
            file.write(f"Take Profit 5 (40%): {self.take_profit5} was hit {self.ProfitsStatus[4]}\n")
            file.write(f"Take Profit 6 (50%): {self.take_profit6} was hit {self.ProfitsStatus[5]}\n")
            file.write(f"Stop Loss 1 (-20%): {self.stop_loss1} was hit {self.ProfitsStatus[6]}\n")
            file.write(f"Stop Loss 2 (-30%): {self.stop_loss2} was hit {self.ProfitsStatus[7]}\n")
            file.write(f"Is successful: {self.Status}\n")
            file.write("-" * 40 + "\n")  # Separator for
