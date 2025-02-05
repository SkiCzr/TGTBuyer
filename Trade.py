
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
        self.entrySum = 0


    #Function that calcualtes the stop losses and take profits based on entryPoint
    def enterPosition(self, entryPrice, entrySum):
        self.entryPrice = entryPrice
        self.entrySum = entrySum
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
