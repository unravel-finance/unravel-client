import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_live_weights(
    portfolio: str,
    API_KEY: str,
    smoothing: str | None = None,
    exchange: str | None = None,
) -> pd.Series:
    """
    Fetch last value of normalized risk signal data from the Unravel API.

    Args:
        portfolio (str): Portfolio Identifier (eg. momentum.20)
        API_KEY (str): The API key to use for the request
        smoothing (str | None): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
        exchange (str | None): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.
    Returns:
        pd.Series: Current weights of the portfolio
    """
    url = f"{BASEAPI}/portfolio/live-weights"
    params = {"portfolio": portfolio}

    if smoothing is not None:
        params["smoothing"] = smoothing
    if exchange is not None:
        params["exchange"] = exchange

    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    series = pd.Series(response["data"], index=response["columns"])
    if response.get("index"):
        series = series.rename(response["index"])
    # Ensure we have a valid Series before calling astype
    if isinstance(series, pd.Series):
        return series.astype(float)
    return pd.Series(response["data"], index=response["columns"]).astype(float)
