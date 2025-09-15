import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_historical_universe(
    size: str,
    start_date: str,
    end_date: str,
    API_KEY: str,
    exchange: str | None = None,
) -> pd.DataFrame:
    """
    Fetch the historical universe from the Unravel API.

    Args:
        size (str): Portfolio size - number of assets to include. Must be one of: 20, 30, or 40
        start_date (str): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
        API_KEY (str): The API key to use for the request
        exchange (str | None): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.

    Returns:
        pd.DataFrame: DataFrame of tickers in the portfolio [True and False]
    """

    url = f"{BASEAPI}/portfolio/universe"
    params = {"size": size, "start_date": start_date, "end_date": end_date}

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
    ).notna()
