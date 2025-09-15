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
    if response.status_code != 200:
        try:
            error_msg = response.json()
        except:
            error_msg = response.text
        raise AssertionError(
            f"Error fetching live weights for {portfolio}, response: {error_msg}"
        )

    response = response.json()
    return (
        pd.Series(response["data"], index=response["columns"])
        .rename(response["index"])
        .astype(float)
    )
