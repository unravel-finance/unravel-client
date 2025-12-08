import pandas as pd
import requests

from .constants import BASEAPI
from .decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_price(
    ticker: str,
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    """
    DEPRECATED: Use get_prices instead, this endpoint will be removed in the future.
    Fetch closing prices for a ticker from the Unravel API.

    Note: This endpoint is deprecated and will only be used for technical integrations.

    Args:
        ticker (str): Ticker symbol (e.g., BTC, ETH)
        api_key (str): The API key to use for the request
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

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        ticker
    )


@retry_on_error(num_trials=3, wait=2.0)
def get_prices(
    tickers: list[str],
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """
    Fetch closing prices for a ticker from the Unravel API.

    Note: This endpoint is deprecated and will only be used for technical integrations.

    Args:
        tickers (list[str]): List of ticker symbols (e.g., ["BTC", "ETH"])
        api_key (str): The API key to use for the request
        start_date (str | None): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str | None): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
    Returns:
        pd.DataFrame: DataFrame of closing prices with datetime index and ticker columns
    """
    url = f"{BASEAPI}/price"
    assert not isinstance(
        tickers, str
    ), "tickers must be a sequence of strings (list, tuple, pandas.Index, etc.)"
    params = {"ticker": ",".join(tickers)}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()

    if "columns" in response:
        return pd.DataFrame(
            response["data"],
            index=pd.to_datetime(response["index"]),
            columns=response["columns"],
        )

    return (
        pd.Series(response["data"], index=pd.to_datetime(response["index"]))
        .rename(tickers[0].replace(",", "").replace(" ", ""))
        .to_frame()
    )
