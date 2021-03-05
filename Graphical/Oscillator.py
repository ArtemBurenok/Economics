import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


class Oscillator:

    def __init__(self, TickerStock, BeginningDate):
        self.stock = yf.download(TickerStock, BeginningDate)
        self.ClosePrice = self.stock[["Adj Close"]]

    def speed_market(self):
        close_change = self.ClosePrice.pct_change()

        close_change.plot()
        plt.show()

    def medium(self):
        close_change = self.ClosePrice.pct_change()
        r_medium1 = close_change.rolling(window=20).mean()
        r_medium2 = close_change.rolling(window=5).mean()
        different = r_medium1 - r_medium2
        different.plot()
        plt.show()

    def stohastic(self):
        max = self.ClosePrice["Adj Close"].max()
        min = self.ClosePrice["Adj Close"].min()
        coeff = 100 * (self.ClosePrice - min) / (max - min)
        coeff.plot()
        plt.show()

    def MAC(self):
        high = self.stock[["High"]]
        low = self.stock[["Low"]]
        high2 = high.rolling(window=25).mean()
        low2 = low.rolling(window=25).mean()
        plt.plot(self.ClosePrice)
        plt.plot(high2)
        plt.plot(low2)
        plt.show()