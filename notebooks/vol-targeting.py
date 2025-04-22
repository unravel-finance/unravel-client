# %%
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from risklab.signal import TargetCalculation, scale_to_target_volatility

sp500 = yf.Ticker("SPY")
sp500_data = sp500.history(period="max")
# 30 day forward return
sp500_data["Forward Return"] = sp500_data["Close"].pct_change(periods=30).shift(-30)

# plot the equity curve

plt.plot(sp500_data["Close"])
plt.show()

# %%
rolling_std = sp500_data["Close"].pct_change().rolling(20).std()
plt.plot(rolling_std)
plt.show()

# %%
rolling_drawdown = sp500_data["Close"] / sp500_data["Close"].rolling(252).max()
plt.plot(rolling_drawdown)
plt.show()


# %% factor plot of SP500 forward returns with rolling drawdown
sns.barplot(x=sp500_data["Forward Return"], y=pd.cut(rolling_drawdown, bins=5))
plt.show()

# %%
sns.barplot(x=sp500_data["Forward Return"], y=pd.cut(rolling_std, bins=5))
plt.show()


# %%
scale_to_target_volatility(
    target_volatility=0.2,
    rolling_window=20,
    returns=sp500_data["Close"].pct_change(),
    upper_limit=1.0,
    method=TargetCalculation.absolute,
    delay=0,
    fill_initial_period_with_mean=False,
)
# %%
