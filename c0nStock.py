# scraper.py

import matplotlib.pyplot as plt
import urllib2
import time
import numpy as np
from debug import *
from scraper import getStockData
from moneyModel import MoneyModel

#CONSTANTS
GRAPH_MODE_ON = True          # Draw a graph to analyzer results?
BACK_TRACK_LENGTH = 5          # How far back into a stock we look to draw the linear line
SLEEP_TIME = 60                # How long to sleep per cycle
STOCK_SWITCH_LENGTH_CYCLES = 5 # How many cycles before the stock is switched out

def addToMap(stockMap, symbol, value):
    if symbol in stockMap:
        stockMap[symbol].append(value)
    else:
        stockMap[symbol] = [value]
        
def calculateSlopePercent(values):
#    for v in values:
#        if v > (values[-1]):
#            return 0
    average = (sum(values[-5:]) / float(len(values[-5:])))
    
    return (values[-1] - values[-5]) / average

def calculatePolyFitFunction(values, degree):
    values = values[-5:]
    average = (sum(values[-5:]) / float(len(values[-5:])))
    x = np.array(list(range(len(values))))
    y = np.array(values)
    coefficents = np.polyfit(x, y, degree)
    polyFunc = np.poly1d(coefficents)

    return polyFunc
    
def calculatePolyFitPercent(values, degree):
    values = values[-5:]
    average = (sum(values[-5:]) / float(len(values[-5:])))
    polyFunc1 = calculatePolyFitFunction(values, 1)
    polyFunc2 = calculatePolyFitFunction(values, 2)
    polyAverage = (polyFunc1(10) + polyFunc2(10)) / 2
    return (polyAverage - average) / average
    
def updateStockMap(stockMap):
    data = getStockData()
    for stock in data:
        (symbol, value) = stock
        addToMap(stockMap, symbol, value)

def determineBestStock(stockMap, fromPoint = -5, toPoint = -1):
    highestStock = "NONE"
    highestSlopePercent = 0.

    for stock in stockMap:
        slopePercent = calculatePolyFitPercent(stockMap[stock][fromPoint:toPoint], 1)
#        slopePercent = calculateSlopePercent(stockMap[stock])
        print stock, slopePercent, stockMap[stock][fromPoint:toPoint]
        if slopePercent >= highestSlopePercent:
            highestStock = stock
            highestSlopePercent = slopePercent 

    return highestStock

def plot(stockNumbers, stockName):
    plt.plot(stockNumbers)
    plt.ylabel("Cost")
    plt.ylabel("Time Minus")
    plt.title(stockName)
    plt.show()
    
if __name__ == "__main__":
    model = MoneyModel()
    stockMap = dict()
    timeCount = 0
    while True:
        updateStockMap(stockMap)

  #      if model.hasStockToSell():
  #          stockName = model.currentStock()
  #          if stockMap[stockName][-1] - stockMap[stockName][-2] < .75:
  #              model.sell(stockMap)
  #              errorMessage("Stock value going down, sold prematurely. ", model)
            
        warningMessage("Time Counter: ", timeCount)
        time.sleep(SLEEP_TIME)
        timeCount += 1

        if timeCount % STOCK_SWITCH_LENGTH_CYCLES == 0:
            stockName = determineBestStock(stockMap)
            infoMessage("Best Stock: ", stockName, " ", stockMap[stockName][-5:])
            if (GRAPH_MODE_ON): plot(stockMap[stockName], stockName)
            
            if model.hasStockToSell():
                model.sell(stockMap)
                goodMessage("After Selling Stock: ", model)

                deltaMoney = model.deltaMoney()
                if deltaMoney > 0:   goodMessage("Delta Money: ", deltaMoney)
                else:                errorMessage("Delta Money: ", deltaMoney)

            model.buy(stockMap, stockName)
            goodMessage("After Buying Stock: ", model)    