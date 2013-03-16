from debug import *

class MoneyModel():
    mCurrentStock = "NONE"
    mNumberStock = 0
    mMoney = 0
    mMoneyHistory = []
    
    def __init__(self, initalMoney = 100000):
        self.mMoney = initalMoney
        self.mMoneyHistory.append(self.mMoney)
        
    def buy(self, stockMap, stockName):
        if (self.mMoney == 0.):
            errorMessage("MoneyModel: you need to sell before you can buy more stock!")
            return

        self.mMoney -= 7
        
        stockValue = stockMap[stockName][-1]
        self.mCurrentStock = stockName
        self.mNumberStock = self.mMoney / stockValue
        self.mMoney = 0

    def sell(self, stockMap):
        if (self.mNumberStock == 0 or self.mCurrentStock == "NONE"):
            errorMessage("MoneyModel: you ain't got no stocks to sell!")
            return
        if (self.mMoney != 0):
            warningMessage("You already have money in the account! money: ", self.mMoney)

        self.mMoney -= 7
        
        stockValue = stockMap[self.mCurrentStock][-1]
        self.mMoney += stockValue * self.mNumberStock
        self.mNumberStock = 0
        self.mCurrentStock = "NONE"
        self.mMoneyHistory.append(self.mMoney)
        
    def deltaMoney(self):
        """Calculate the amount of money made on previous stock"""
        previousMoney = self.mMoneyHistory[-2]
        currentMoney = self.mMoneyHistory[-1]
        return currentMoney - previousMoney

    def hasStockToSell(self):
        return self.mNumberStock != 0

    def __str__(self):
        out = "Money: " +  str(self.mMoney) + "\t" + str(self.mCurrentStock) + "-" + str(self.mNumberStock)
        return out

    def currentStock(self):
        return self.mCurrentStock
        
if __name__ == "__main__":
    model = MoneyModel()

    stockMap = { "AA" : [5], "BB": [6] }
    model.buy(stockMap, "AA")
    print model

    stockMap["AA"].append(7)
    model.sell(stockMap)
    print model

    print model.deltaMoney()