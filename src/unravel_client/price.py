import pandas as pd
import requests

from .constants import BASEAPI
from .decorators import handle_api_errors


@handle_api_errors
def get_price(
    ticker: str,
    API_KEY: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    """
    Fetch closing prices for a ticker from the Unravel API.

    Note: This endpoint is deprecated and will only be used for technical integrations.

    Args:
        ticker (str): Ticker symbol (e.g., BTC, ETH)
        API_KEY (str): The API key to use for the request
        start_date (str | None): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str | None): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
    Returns:
        pd.Series: Time series of closing prices with datetime index
    """
    url = f"{BASEAPI}/price"
    params = {"ticker": ticker}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        ticker
    )
