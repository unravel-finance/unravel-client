import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_portfolio_historical_weights(
    portfolio: str,
    API_KEY: str,
    start_date: str | None = None,
    end_date: str | None = None,
    smoothing: str | None = None,
    exchange: str | None = None,
) -> pd.DataFrame:
    """
    Fetch normalized risk signal data from the Unravel API.

    Args:
        portfolio (str): Portfolio Identifier (eg. momentum.20)
        API_KEY (str): The API key to use for the request
        start_date (str | None): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str | None): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
        smoothing (str | None): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
        exchange (str | None): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.
    Returns:
        pd.DataFrame: Historical weights of the portfolio
    """
    url = f"{BASEAPI}/portfolio/historical-weights"
    params = {"portfolio": portfolio}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if smoothing is not None:
        params["smoothing"] = smoothing
    if exchange is not None:
        params["exchange"] = exchange

    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    ).astype(float)
