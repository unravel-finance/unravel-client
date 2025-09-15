import pandas as pd
import requests

from ..constants import BASEAPI


def get_normalized_series(
    ticker: str,
    series: str,
    API_KEY: str,
    start_date: str | None = None,
    end_date: str | None = None,
    smoothing: int | str | None = None,
) -> pd.Series:
    """
    Fetch normalized directional factor or risk signal data from the Unravel API.

    Args:
        ticker (str): The cryptocurrency ticker symbol (e.g., 'BTC')
        series (str): The normalized directional factor series to retrieve (e.g., 'meta_risk')
        API_KEY (str): The API key to use for the request
        start_date (str | None): Start date in 'YYYY-MM-DD' format
        end_date (str | None): End date in 'YYYY-MM-DD' format
        smoothing (int | None): The smoothing window to use for the directional factor,
            if None, the default smoothing window will be used.
    Returns:
        pd.Series: Time series of the normalized directional factor with datetime index
    """
    url = f"{BASEAPI}/normalized-series"
    params = {
        "ticker": ticker,
        "series": series,
        "start_date": start_date,
        "end_date": end_date,
    }
    if smoothing is not None:
        params["smoothing"] = str(smoothing)
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        ticker
    )
