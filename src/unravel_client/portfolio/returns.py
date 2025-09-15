import pandas as pd
import requests

from ..constants import BASEAPI


def get_portfolio_returns(
    portfolioId: str,
    API_KEY: str,
    start_date: str | None = None,
    end_date: str | None = None,
    smoothing: str | None = None,
) -> pd.Series:
    """
    Fetch portfolio returns from the Unravel API.

    Args:
        portfolioId (str): The portfolio ID
        API_KEY (str): The API key to use for the request
        start_date (str, optional): Start date in YYYY-MM-DD format
        end_date (str, optional): End date in YYYY-MM-DD format
        smoothing (str, optional): Smoothing window
    Returns:
        pd.Series: Portfolio returns data
    """
    url = f"{BASEAPI}/portfolio/returns"
    params = {"portfolio": portfolioId}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if smoothing:
        params["smoothing"] = smoothing

    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        try:
            error_msg = response.json()
        except:
            error_msg = response.text
        raise AssertionError(
            f"Error fetching returns for {portfolioId}, response: {error_msg}"
        )

    response = response.json()
    # The returns API returns just the index, we need to create a series with zeros or fetch actual data
    # For now, return a series with the index and zero values
    return pd.Series(
        0.0,  # Placeholder values
        index=pd.to_datetime(response["index"]),
        name="returns",
    )
