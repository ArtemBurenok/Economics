import numpy as np
import yfinance as yf


class Ratio:

    def __init__(self, StockTicker, BenchmarkTicker, Date):
        StockPrice = yf.download(StockTicker, Date)
        BenchmarkPrice = yf.download(BenchmarkTicker, Date)
        self.PriceStockChange = StockPrice.pct_change()
        self.PriceBenchmarkChange = BenchmarkPrice.pct_change()
        self.RiskPremium = np.mean(self.PriceStockChange - self.PriceBenchmarkChange)

    def RatioSharp(self):
        Risk = np.std(self.PriceStockChange)
        return self.RiskPremium / Risk

    def Beta(self):
        FactorStock = self.PriceStockChange - np.mean(self.PriceStockChange)
        FactorBenchmark = self.PriceBenchmarkChange - np.mean(self.PriceBenchmarkChange)
        return np.mean(FactorBenchmark * FactorStock) / (np.var(self.PriceStockChange) / 100)

    def RatioTraynor(self):
        return self.RiskPremium / self.Beta()

    def RatioSortino(self):
        Damages = []
        Array = np.array(self.PriceStockChange)
        for i in range(len(Array)):
            if Array[i] < 0:
                Damages.append(Array[i])
        return self.RiskPremium / np.std(Damages)

    def RatioModigliani(self):
        return self.RiskPremium * (np.std(self.PriceBenchmarkChange) / np.std(self.PriceStockChange)) \
        + self.PriceBenchmarkChange

    def RatioKalmar(self):
        MaxDrawdown = max(self.PriceStockChange) - min(self.PriceStockChange)
        GeometricMeanIncome = np.prod(self.PriceStockChange) ** (1/len(self.PriceStockChange))
        return GeometricMeanIncome / MaxDrawdown

