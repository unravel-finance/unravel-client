import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_live_weights(
    id: str,
    api_key: str,
    smoothing: str | None = None,
    exchange: str | None = None,
) -> pd.Series:
    """
    Fetch last value of normalized risk signal data from the Unravel API.

    Args:
        id (str): Portfolio Identifier (eg. momentum.20)
        api_key (str): The API key to use for the request
        smoothing (str | None): Portfolio smoothing window for the data. Portfolio smoothing window for the data. Valid values and default smoothing for each portfolio can be found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)
        exchange (str | None): Exchange constraint for portfolio data. Valid options are found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)
    Returns:
        pd.Series: Current weights of the portfolio
    """
    url = f"{BASEAPI}/portfolio/live-weights"
    params = {"portfolio": id}

    if smoothing is not None:
        params["smoothing"] = smoothing
    if exchange is not None:
        params["exchange"] = exchange

    headers = {"X-API-KEY": api_key}
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
