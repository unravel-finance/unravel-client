# %%
import os
import requests
import pandas as pd
import datetime

import matplotlib.pyplot as plt


def vectorized_backtest(
    price_series: pd.Series, signal_series: pd.Series, transaction_cost: float = 0.0005
) -> pd.DataFrame:
    """
    Perform a vectorized backtest on price and signal series.

    Args:
        price_series (pd.Series): Price series of the asset
        signal_series (pd.Series): Signal series between -1 and 1
        transaction_cost (float): Transaction cost as a decimal (e.g., 0.001 for 0.1%)

    Returns:
        pd.DataFrame: DataFrame containing positions, returns, and cumulative returns
    """
    # Forward fill missing values
    price_series = price_series.ffill()
    signal_series = signal_series.ffill()

    # Calculate position changes (when signal changes)
    position_changes = signal_series.diff()

    # Calculate returns including transaction costs
    returns = price_series.pct_change()
    position_returns = (
        signal_series.shift(1) * returns
    )  # Shift to avoid look-ahead bias

    # Apply transaction costs only when position changes
    transaction_costs = abs(position_changes) * transaction_cost

    # Calculate net returns
    net_returns = position_returns - transaction_costs

    # Calculate cumulative returns
    cumulative_returns = (1 + net_returns).cumprod()

    # Create results DataFrame
    return pd.DataFrame(
        {
            "price": price_series,
            "signal": signal_series,
            "position": signal_series,
            "position_changes": position_changes,
            "returns": returns,
            "position_returns": position_returns,
            "transaction_costs": transaction_costs,
            "net_returns": net_returns,
            "cumulative_returns": cumulative_returns,
            "price_rebased": (price_series / price_series.iloc[0]),
        }
    )


def get_normalized_series(
    ticker: str, series: str, start_date: str, end_date: str
) -> pd.Series:
    """
    Fetch normalized risk signal data from the Unravel API.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., 'BTC')
        series (str): The risk factor series to retrieve (e.g., 'meta_risk')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.Series: Time series of the risk signal with datetime index
    """
    url = "https://unravel.finance/api/v1/normalized-series"
    params = {
        "ticker": ticker,
        "series": series,
        "start_date": start_date,
        "end_date": end_date,
    }
    headers = {"X-API-KEY": os.environ.get("UNRAVEL_API_KEY")}
    response = requests.get(url, headers=headers, params=params)
    assert (
        response.status_code == 200
    ), f"Error fetching exogenous series for {ticker} and {series}, response: {response.json()}"

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        ticker
    )


def get_price_series(ticker: str, start_date: str, end_date: str) -> pd.Series:
    """
    Fetch the price series from the Unravel API.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., 'BTC')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.Series: Time series of the risk signal with datetime index
    """
    url = "https://unravel.finance/api/v1/price-series"
    params = {"ticker": ticker, "start_date": start_date, "end_date": end_date}
    headers = {"X-API-KEY": os.environ.get("UNRAVEL_API_KEY")}
    response = requests.get(url, headers=headers, params=params)
    assert (
        response.status_code == 200
    ), f"Error fetching price series for {ticker}, response: {response.json()}"

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        ticker
    )


def get_signal_with_backtest(
    ticker: str, risk_factor: str, start_date: str, end_date: str
) -> pd.DataFrame:
    """
    Fetch risk signal and price data, then perform a backtest.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., 'BTC')
        risk_factor (str): The risk factor to use as trading signal (e.g., 'meta_risk')
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.DataFrame: Backtest results including positions, returns, and performance metrics
    """
    risk_factor_signal = get_normalized_series(
        ticker, risk_factor, start_date, end_date
    )
    price = get_price_series(ticker, start_date, end_date)
    price = price.reindex(risk_factor_signal.index)
    return vectorized_backtest(price, risk_factor_signal)


def plot_backtest_results(
    results: pd.DataFrame, ticker: str, risk_factor: str, figsize=(12, 10)
):
    """
    Plot backtest results with performance chart and signal.

    Args:
        results (pd.DataFrame): DataFrame containing backtest results with
                               'cumulative_returns', 'price_rebased', and 'signal' columns
        figsize (tuple): Figure size as (width, height) in inches
    """
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=figsize, gridspec_kw={"height_ratios": [2, 1]}
    )

    ax1.plot(results.index, results["cumulative_returns"], label="Strategy Returns")
    ax1.plot(results.index, results["price_rebased"], label=f"Benchmark ({ticker})")
    ax1.set_title("Performance with Risk Signal", fontsize=14)
    ax1.legend()
    ax1.grid(True, axis="y", linestyle="--")

    ax2.plot(results.index, results["signal"], label="Signal", color="orange")
    ax2.set_title(f"Risk Signal {risk_factor}")
    ax2.legend()
    ax2.grid(True, axis="y", linestyle="--")

    plt.tight_layout()
    plt.show()

    return fig, (ax1, ax2)


risk_factor = "meta_risk"
ticker = "BTC"
start_date = "2023-01-01"
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

results = get_signal_with_backtest(ticker, risk_factor, start_date, end_date)
plot_backtest_results(results, ticker, risk_factor)

# %%
