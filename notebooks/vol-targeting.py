# %%
from typing import Any

from pandas.core.frame import DataFrame
from pandas.core.series import Series
from tabulate import tabulate


import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from risklab.backtest import backtest_signal
from risklab.returns import rebase, to_prices
from risklab.signal import scale_to_target_volatility
from risklab.stats import sharpe, to_drawdown_series

sp500 = yf.Ticker("SPY")
sp500_data = sp500.history(period="max")["2005-01-01":]

# 30 day forward return
sp500_data["30 Day Forward Return"] = (
    sp500_data["Close"].pct_change(periods=30).shift(-31)
)

# %%
rolling_volatility: Any | DataFrame | Series = sp500_data["Close"].pct_change().rolling(
    20
).std() * np.sqrt(252)
plt.plot(rolling_volatility)
plt.show()

# %%
rolling_drawdown = sp500_data["Close"].div(sp500_data["Close"].rolling(252).max()) * 100
plt.plot(rolling_drawdown)
plt.show()


# %% factor plot of SP500 forward returns with rolling drawdown
sns.barplot(
    x=sp500_data["30 Day Forward Return"],
    y=pd.cut(rolling_drawdown, bins=5).rename("Drawdown"),
)
plt.show()

# %% factor plot of SP500 forward returns with rolling volatility
sns.barplot(
    x=sp500_data["30 Day Forward Return"],
    y=pd.cut(rolling_volatility, bins=5).rename("Annualized Volatility"),
)
plt.show()


# %%
vol_signal = scale_to_target_volatility(
    target_volatility=0.16 / np.sqrt(252),
    rolling_window=30,
    returns=sp500_data["Close"].pct_change(),
    upper_limit=2.0,
    delay=0,
    fill_initial_period_with_mean=False,
)
results = backtest_signal(
    signal=vol_signal,
    underlying=sp500_data["Close"].pct_change(),
    transaction_cost=0.001,
    lag=0,
)

plt.figure(figsize=(12, 8))
plt.subplot2grid((5, 1), (0, 0), rowspan=3)
plt.plot(rebase(to_prices(results.returns)), label="Risk Managed Strategy")
plt.plot(rebase(sp500_data["Close"].loc[results.returns.index]), label="SP500")
plt.legend()
plt.title("Performance Comparison")

plt.subplot2grid((5, 1), (3, 0), rowspan=1)
plt.plot(vol_signal)
plt.title("Volatility Signal")
plt.tight_layout()
plt.show()

# %% print sharpe ratio, volatility, max drawdown for both results and sp500_data as a table

# Calculate metrics for risk managed strategy
risk_managed_sharpe = round(sharpe(results.returns, 252), 2)
risk_managed_volatility = round(results.returns.std() * np.sqrt(252), 2)
risk_managed_max_dd = round(to_drawdown_series(results.returns).min(), 2)

# Calculate metrics for SP500
sp500_returns = sp500_data["Close"].pct_change()
sp500_sharpe = round(sharpe(sp500_returns, 252), 2)
sp500_volatility = round(sp500_returns.std() * np.sqrt(252), 2)
sp500_max_dd = round(to_drawdown_series(sp500_returns).min(), 2)

# Create and display table
metrics_table = [
    ["Metric", "Risk Managed Strategy", "SP500"],
    ["Sharpe Ratio", risk_managed_sharpe, sp500_sharpe],
    ["Volatility", risk_managed_volatility, sp500_volatility],
    ["Max Drawdown", risk_managed_max_dd, sp500_max_dd],
]

print(tabulate(metrics_table, headers="firstrow", tablefmt="grid"))

# %%
