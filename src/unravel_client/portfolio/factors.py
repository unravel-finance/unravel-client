import pandas as pd
import requests

from ..constants import BASEAPI


def get_portfolio_factors_historical(
    portfolioId: str,
    tickers: list[str],
    API_KEY: str,
) -> pd.DataFrame:
    """
    Fetch historical factors for a portfolio from the Unravel API.

    Args:
        portfolioId (str): The portfolio ID
        tickers (list[str]): List of tickers in the portfolio
        API_KEY (str): The API key to use for the request
    Returns:
        pd.DataFrame: Historical factor data for the input tickers
    """
    url = f"{BASEAPI}/portfolio/factors"
    params = {"id": portfolioId, "tickers": ",".join(tickers)}
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    ).astype(float)
