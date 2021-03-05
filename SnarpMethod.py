import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

Price = yf.download(["IBM", "GE", "T", "KO"], period="3mo")
ClosePrice = Price.Close

DeltaClosePrice = ClosePrice.pct_change()

Mean = DeltaClosePrice.mean() # Средняя доходность
cov = DeltaClosePrice.cov() # Ковариационная матрица

cnt = len(DeltaClosePrice.columns)


def randPortfolio(): # Случайный портфель (доли)
    res = np.exp(np.random.randn(cnt))
    res = res / res.sum()
    return res


def IncomePortfolio(Rand):
    return np.matmul(Mean.values, Rand)


def RiskPortfolio(Rand):
    return np.matmul(np.matmul(Rand, cov.values), Rand)


N = 4000
Risk = np.zeros(N)
Income = np.zeros(N)
Portfolio = np.zeros((N, cnt))

for i in range(N):
    rand = randPortfolio()

    Portfolio[i, :] = rand
    Risk[i] = RiskPortfolio(rand)
    Income[i] = IncomePortfolio(rand)

plt.figure(figsize=(10, 8))

plt.scatter(Risk * 100, Income * 100, c="y", marker=".")
plt.xlabel("риск, %")
plt.ylabel("доходность, %")
plt.title("Облако портфелей")

MinRisk = np.argmin(Risk)
plt.scatter([Risk[MinRisk] * 100], [Income[MinRisk] * 100], c="r", marker="*", label="Минимальный риск")

MaxSharpCoefficient = np.argmax(Income / Risk)
plt.scatter([Risk[MaxSharpCoefficient] * 100], [Income[MaxSharpCoefficient] * 100], c="g", marker="o",
label="Максимальый коэффицент Шарпа")

RiskMin = np.ones(cnt) / cnt
RiskMean = RiskPortfolio(RiskMin)
IncomeMean = IncomePortfolio(RiskMin)
plt.scatter(RiskMean * 100, IncomeMean * 100, c="b", marker="x", label="Усреднённый портфель")

plt.legend()

plt.show()


print('--------— Максимальный коэффициент Шарпа —--------')
print()
print("риск = " + str((float(Risk[MaxSharpCoefficient])*100.)))
print("доходность = " + str((float(Income[MaxSharpCoefficient])*100.)))
print()
print(pd.DataFrame([Portfolio[MaxSharpCoefficient]*100], columns=DeltaClosePrice.columns, index=['доли, %']).T)
print()
