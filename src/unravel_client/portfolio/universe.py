import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_historical_universe(
    size: str,
    api_key: str,
    start_date: str,
    end_date: str,
    exchange: str | None = None,
) -> pd.DataFrame:
    """
    Fetch the historical universe from the Unravel API.

    Args:
        size (str): Portfolio size - number of assets to include. Must be one of: 20, 30, or 40
        api_key (str): The API key to use for the request
        start_date (str): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
        exchange (str | None): Exchange constraint for portfolio data. Valid options are found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)

    Returns:
        pd.DataFrame: DataFrame of tickers in the portfolio [True and False]
    """

    url = f"{BASEAPI}/portfolio/universe"
    params = {"size": size, "start_date": start_date, "end_date": end_date}

    if exchange is not None:
        params["exchange"] = exchange

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    ).notna()
