# %%
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sp500 = yf.Ticker("SPY")
sp500_data = sp500.history(period="max")
# 30 day forward return
sp500_data["Forward Return"] = sp500_data["Close"].pct_change(periods=1).shift(-1)

# plot the equity curve

plt.plot(sp500_data["Close"])
plt.show()

# %%
rolling_std = sp500_data["Close"].pct_change().rolling(20).std()
plt.plot(rolling_std)
plt.show()


# %% measure the velocity of the volatility
sp500_data["Vol Velocity"] = rolling_std.pct_change(30)
plt.plot(sp500_data["Vol Velocity"])
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
sns.barplot(
    x=sp500_data["Forward Return"], y=pd.cut(sp500_data["Vol Velocity"], bins=5)
)
plt.show()

# %%
