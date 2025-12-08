import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_portfolio_returns(
    id: str,
    api_key: str,
    smoothing: str | None = None,
    exchange: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    """
    Fetch portfolio returns from the Unravel API.

    Args:
        id (str): Portfolio Identifier (eg. momentum.20)
        api_key (str): The API key to use for the request
        smoothing (str | None): Portfolio smoothing window for the data. Portfolio smoothing window for the data. Valid values and default smoothing for each portfolio can be found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)
        exchange (str | None): Exchange constraint for portfolio data. Valid options are found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)
        start_date (str | None): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str | None): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
    Returns:
        pd.Series: Portfolio returns data
    """
    url = f"{BASEAPI}/portfolio/returns"
    params = {"portfolio": id}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if smoothing is not None:
        params["smoothing"] = smoothing
    if exchange is not None:
        params["exchange"] = exchange

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()

    return pd.Series(
        response["data"],
        index=pd.to_datetime(response["index"]),
        name="returns",
    ).astype(float)
