import pandas as pd
import requests

from ..constants import BASEAPI


def get_portfolio_historical_weights(
    portfolio: str,
    API_KEY: str,
    start_date: str | None = None,
    end_date: str | None = None,
    smoothing: str | None = None,
) -> pd.DataFrame:
    """
    Fetch normalized risk signal data from the Unravel API.

    Args:
        portfolio (str): The portfolio ID
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        API_KEY (str): The API key to use for the request
    Returns:
        pd.DataFrame: Historical weights of the portfolio
    """
    url = f"{BASEAPI}/portfolio/historical-weights"
    params = {
        "portfolio": portfolio,
        "start_date": start_date,
        "end_date": end_date,
        "smoothing": smoothing,
    }
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        try:
            error_msg = response.json()
        except:
            error_msg = response.text
        raise AssertionError(
            f"Error fetching portfolio for {portfolio}, response: {error_msg}"
        )

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
        columns=response["columns"],
    ).astype(float)
