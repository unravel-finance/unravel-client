import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_risk_overlay(
    portfolio: str,
    overlay: str,
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    """
    Retrieve historical risk overlay data for a portfolio.

    Args:
        portfolio: Portfolio ID (see [Unravel Catalog](https://unravel.finance/home/api/catalog/portfolios))
        overlay: Risk overlay ID (see [Unravel Catalog](https://unravel.finance/home/api/catalog/risk-overlays))
        api_key: API authentication key
        start_date: Optional filter start date in YYYY-MM-DD format
        end_date: Optional filter end date in YYYY-MM-DD format

    Returns:
        pd.Series: Series with datetime index and float values representing
                      historical risk overlay values for each timestamp

    Raises:
        APIError: If the API request fails or returns an error status
    """
    url = f"{BASEAPI}/portfolio/risk-overlay"
    params = {"portfolio": portfolio, "overlay": overlay}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(
        response["data"],
        index=pd.to_datetime(response["index"]),
    ).astype(float)


@retry_on_error(num_trials=3, wait=2.0)
def get_risk_overlay_live(
    portfolio: str,
    overlay: str,
    api_key: str,
) -> pd.Series:
    """
    Retrieve the latest risk overlay value for a portfolio.

    Args:
        portfolio: Portfolio ID (see [Unravel Catalog](https://unravel.finance/home/api/catalog/portfolios))
        overlay: Risk overlay ID (see [Unravel Catalog](https://unravel.finance/home/api/catalog/risk-overlays))
        api_key: API authentication key

    Returns:
        pd.Series: Series with datetime index and float values representing
                   latest risk overlay value

    Raises:
        APIError: If the API request fails or returns an error status
    """
    url = f"{BASEAPI}/portfolio/risk-overlay-live"
    params = {"portfolio": portfolio, "overlay": overlay}

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()
    return pd.Series(
        [response["data"]],
        index=[pd.to_datetime(response["index"])],
    ).astype(float)


@retry_on_error(num_trials=3, wait=2.0)
def get_risk_regime(
    overlay: str,
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    """
    Retrieve historical risk regime data.

    Args:
        overlay: Risk overlay ID (see [Unravel Catalog](https://unravel.finance/home/api/catalog/risk-overlays))
        api_key: API authentication key
        start_date: Optional filter start date in YYYY-MM-DD format
        end_date: Optional filter end date in YYYY-MM-DD format

    Returns:
        pd.Series: Series with datetime index and float values representing
                   historical risk regime values for each timestamp

    Raises:
        APIError: If the API request fails or returns an error status
    """
    url = f"{BASEAPI}/risk-regime"
    params = {"overlay": overlay}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.Series(
        response["data"],
        index=pd.to_datetime(response["index"]),
    ).astype(float)


@retry_on_error(num_trials=3, wait=2.0)
def get_risk_regime_live(
    overlay: str,
    api_key: str,
) -> pd.Series:
    """
    Retrieve the latest market-wide risk regime value.

    Args:
        overlay: Risk overlay ID (see [Unravel Catalog](https://unravel.finance/home/api/catalog/risk-overlays))
        api_key: API authentication key

    Returns:
        pd.Series: Series with datetime index and float values representing
                   latest risk regime value

    Raises:
        APIError: If the API request fails or returns an error status
    """
    url = f"{BASEAPI}/risk-regime-live"
    params = {"overlay": overlay}

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()

    return pd.Series(
        [response["data"]],
        index=[pd.to_datetime(response["index"])],
    ).astype(float)
