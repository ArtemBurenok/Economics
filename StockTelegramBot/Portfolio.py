import yfinance as yf
import numpy as np
import pandas as pd


class Portfolio:

    def __init__(self, tickers):
        Price = yf.download(tickers, period="3mo")
        ClosePrice = Price.Close

        DeltaClosePrice = ClosePrice.pct_change()

        self.Mean = DeltaClosePrice.mean()  # Средняя доходность
        self.cov = DeltaClosePrice.cov()  # Ковариационная матрица

        self.cnt = len(DeltaClosePrice.columns)

        N = 4000
        Risk = np.zeros(N)
        Income = np.zeros(N)
        Portfolio = np.zeros((N, self.cnt))

        for i in range(N):
            rand = self.randPortfolio()

            Portfolio[i, :] = rand
            Risk[i] = self.RiskPortfolio(rand)
            Income[i] = self.IncomePortfolio(rand)

        MaxSharpCoefficient = np.argmax(Income / Risk)
        self.Data = pd.DataFrame([Portfolio[MaxSharpCoefficient] * 100], columns=DeltaClosePrice.columns, index=['Доли, %']).T

    def randPortfolio(self):  # Случайный портфель (доли)
        res = np.exp(np.random.randn(self.cnt))
        res = res / res.sum()
        return res

    def IncomePortfolio(self, Rand):
        return np.matmul(self.Mean.values, Rand)

    def RiskPortfolio(self, Rand):
        return np.matmul(np.matmul(Rand, self.cov.values), Rand)

    def ReturnPortfolio(self):
        return self.Data

