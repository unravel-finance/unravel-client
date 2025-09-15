import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_historical_universe(
    size: str, start_date: str, end_date: str, API_KEY: str
) -> pd.DataFrame:
    """
    Fetch the historical universe from the Unravel API.

    Args:
        size (str): The universe size to use for the request. Pass in 'full' to get all available tickers for the portfolio.
        start_date (str): The start date to use for the request.
        end_date (str): The end date to use for the request.
        API_KEY (str): The API key to use for the request

    Returns:
        pd.DataFrame: DataFrame of tickers in the portfolio [True and False]
    """

    url = f"{BASEAPI}/portfolio/universe"
    params = {"size": size, "start_date": start_date, "end_date": end_date}

    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    ).notna()
