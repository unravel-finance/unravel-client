import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_portfolio_factors_historical(
    id: str,
    tickers: list[str],
    api_key: str,
    smoothing: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """
    Fetch historical factors for a portfolio from the Unravel API.

    Args:
        id (str): Portfolio Factor Identifier without the universe specifier (eg. momentum instead of momentum.20)
        tickers (list[str]): List of tickers in the portfolio
        api_key (str): The API key to use for the request
        smoothing (str | None): Portfolio smoothing window for the data. Valid values and default smoothing for each portfolio can be found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)
        start_date (str | None): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str | None): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
    Returns:
        pd.DataFrame: Historical factor data for the input tickers
    """
    url = f"{BASEAPI}/portfolio/factors"
    params = {"id": id, "tickers": ",".join(tickers)}

    if smoothing is not None:
        params["smoothing"] = smoothing
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    ).astype(float)


@retry_on_error(num_trials=3, wait=2.0)
def get_portfolio_factors_live(
    id: str,
    tickers: list[str],
    api_key: str,
    smoothing: str | None = None,
) -> pd.Series:
    """
    Fetch the latest factor data for specific tickers within a single factor portfolio.

    Args:
        id (str): Portfolio Factor Identifier without the universe specifier (eg. momentum instead of momentum.20)
        tickers (list[str]): List of tickers in the portfolio
        api_key (str): The API key to use for the request
        smoothing (str | None): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
    Returns:
        pd.Series: Latest factor data for the specified tickers
    """
    url = f"{BASEAPI}/portfolio/factors-live"
    params = {"id": id, "tickers": ",".join(tickers)}

    if smoothing is not None:
        params["smoothing"] = smoothing

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(
        response["data"], index=response["columns"], name=response["index"]
    ).astype(float)
