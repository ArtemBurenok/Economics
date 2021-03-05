import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


class GraphicalAnalysis:

    def __init__(self, TickerStock, TickerBond, BeginingDate):
        self.stock = yf.download(TickerStock, BeginingDate)
        self.bond = yf.download(TickerBond, BeginingDate)

    def Histograma(self):
        daily_close = self.stock[['Adj Close']]  # Цена закрытия
        daily_pct_change = daily_close.pct_change(10)  # Дневная доходность

        daily_pct_change.hist(bins=50)  # Построение гистограммы
        plt.show()

    def Volality(self):
        daily_close = self.stock[['Adj Close']]  # Цена закрытия
        daily_pct_change = daily_close.pct_change()  # Дневная доходность
        min_periods = 100

        vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)  # Волатильность
        vol.plot(figsize=(10, 10))

        plt.show()

    def RollingMedium(self):
        close_prise = self.stock['Adj Close']

        self.stock['40'] = close_prise.rolling(window=10).mean()  # Вычисление скользящей средней 40 дней
        self.stock[['Adj Close', '40']].plot(figsize=(20, 20))  # Построение данных

        plt.show()
