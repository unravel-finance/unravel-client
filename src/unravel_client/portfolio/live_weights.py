import pandas as pd
import requests

from ..constants import BASEAPI


def get_live_weights(portfolio: str, API_KEY: str) -> pd.Series:
    """
    Fetch last value of normalized risk signal data from the Unravel API.

    Args:
        portfolio (str): The portfolio ID
        API_KEY (str): The API key to use for the request
    Returns:
        pd.Series: Current weights of the portfolio
    """
    url = f"{BASEAPI}/portfolio/live-weights"
    params = {
        "portfolio": portfolio,
    }
    headers = {"X-API-KEY": API_KEY}
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
