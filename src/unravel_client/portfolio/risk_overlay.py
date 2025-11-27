import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_risk_overlay(
    portfolio: str,
    overlay: str,
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
    smoothing: str | None = None,
) -> pd.Series:
    """
    Fetch normalized directional factor or risk signal data from the Unravel API.

    Args:
        portfolio (str): Portfolio identifier (e.g., momentum.20)
        overlay (str): Overlay to retrieve (e.g., crypto_trend_consensus)
        api_key (str): The API key to use for the request
        start_date (str | None): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
        end_date (str | None): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
        smoothing (str | None): Smoothing window for the data. Valid values are "default", "0", "7", "30". Default is "default".
    Returns:
        pd.Series: Time series of the normalized directional factor with datetime index
    """
    url = f"{BASEAPI}/risk-overlay"
    params = {
        "portfolio": portfolio,
        "overlay": overlay,
    }

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if smoothing is not None:
        params["smoothing"] = smoothing

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(response["data"], index=pd.to_datetime(response["index"])).rename(
        overlay
    )
