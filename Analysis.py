import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class GraphicalAnalysis():

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

class RatioAnalysis():

    def __init__(self, TickerStock, TickerBond, BeginingDate):
        self.stock = yf.download(TickerStock, BeginingDate)
        self.bond = yf.download(TickerBond, BeginingDate)

    def RatioTraynor(self):
        s_close = self.stock[['Adj Close']]
        stock_close_change = s_close.pct_change()  # Доход

        b_close = self.bond[['Adj Close']]
        bond_close_change = b_close.pct_change()  # Доход

        stock_change_medium = np.mean(stock_close_change)  # Среднее доходности акции
        factor_stock = stock_close_change - stock_change_medium  # 1 множитель

        bond_change_medium = np.mean(bond_close_change)  # Среднее доходности облигаций
        factor_bond = bond_close_change - bond_change_medium

        covariation = np.mean(factor_stock * factor_bond)  # Ковариация
        variable = np.std(stock_close_change)  # Дисперсия
        beta = covariation / variable  # Бета коэффицент(Волатильность бумаг по отношению к безрисковой ставке)
        beta = float(beta)
        print(f'Бета-коэффицент: {beta}')

        change_medium = stock_change_medium - bond_change_medium
        ratio = change_medium / beta
        ratio = float(ratio)

        print(f"Коэффицент Трейнора: {ratio}")  # Показывает превышение безрисковой ставки над бета риском

    def RatioSharp(self):
        close = self.stock[['Adj Close']]
        close_change = close.pct_change()  # Доходность акции

        r_close = self.bond[['Adj Close']]
        r_close_change = r_close.pct_change()  # Доходность облигаций

        math_wait = np.mean(close_change)  # Мат. ожидание акции
        r_math_wait = np.mean(r_close_change)  # Мат. ожидание облигаций
        dif_wait = math_wait - r_math_wait

        medium_change = np.std(close_change)
        ratio = dif_wait / medium_change
        ratio = float(ratio)
        print(f"Коэффицет Шарпа: {ratio}")

    def RatioInf(self):
        s_close = self.stock[['Adj Close']]
        stock_close_change = s_close.pct_change()  # Доход

        b_close = self.bond[['Adj Close']]
        bond_close_change = b_close.pct_change()  # Доход

        medium_close_stock = np.mean(stock_close_change)
        medium_close_bond = np.mean(bond_close_change)

        dif_close = medium_close_stock - medium_close_bond
        medium_change = np.std(stock_close_change - bond_close_change)
        ratio = dif_close / medium_change
        ratio = float(ratio)

        print(
            f"Информационный коэффицент: {ratio}")  # Показывает насколько доход отличнен от бенчмарка 1-идеальная зависимость, 0-нет

    def RatioModiliany(self):
        s_close = self.stock[['Adj Close']]
        stock_close_change = s_close.pct_change()  # Доход

        b_close = self.bond[['Adj Close']]
        bond_close_change = b_close.pct_change()  # Доход

        medium_close_stock = np.mean(stock_close_change)  # Средние значения дохода
        medium_close_bond = np.mean(bond_close_change)

        variable_s = np.var(stock_close_change)  # Дисперсии доходов
        variable_b = np.var(bond_close_change)

        factor_1 = medium_close_stock - medium_close_bond  # Множители
        factor_2 = variable_s / variable_b

        ratio = factor_1 * factor_2 - medium_close_bond
        ratio = float(ratio)
        print(f"Коэффицент Модильяни: {ratio}")  # Коэффициент позволяет оценить эффективность одного портфеля относительно другого за определенный период

class CAPM():

    def __init__(self, TickerStock, TickerBenchmark, BeginDate):
        stock = yf.download(TickerStock, BeginDate)
        self.stock = stock[["Adj Close"]]
        self.benchmark = yf.download(TickerBenchmark, BeginDate)
        self.RiskFree = self.benchmark[["Adj Close"]]
        CloseChange = self.stock.pct_change(90)
        self.DeltaIncome = CloseChange - self.RiskFree

    def Beta(self):
        factorDelta = self.DeltaIncome - np.mean(self.DeltaIncome)
        factorRiskFree = self.RiskFree - np.mean(self.RiskFree)

        covariation = np.mean(factorDelta * factorRiskFree)
        variable = np.std(self.DeltaIncome)

        beta = covariation / variable
        return beta

    def CAPM(self):
        return self.RiskFree + self.Beta()

class Oscilator():

    def __init__(self, TickerStock, BeginingDate):
        self.stock = yf.download(TickerStock, BeginingDate)
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
