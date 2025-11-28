import pandas as pd
import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_risk_overlays(
    portfolio: str,
    risk: str,
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    url = f"{BASEAPI}/portfolio/risk-overlay"
    params = {"portfolio": portfolio, "risk": risk}

    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return pd.DataFrame(
        response["data"],
        index=pd.to_datetime(response["index"]),
    ).astype(float)


@handle_api_errors
def get_risk_overlays_live(
    portfolio: str,
    risk: str,
    api_key: str,
) -> float:
    url = f"{BASEAPI}/portfolio/risk-overlay-live"
    params = {"portfolio": portfolio, "risk": risk}

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return response["data"]


@handle_api_errors
def get_risk_regime(
    risk: str,
    api_key: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.Series:
    url = f"{BASEAPI}/risk-regime"
    params = {"risk": risk}

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


@handle_api_errors
def get_risk_regime_live(
    risk: str,
    api_key: str,
) -> float:
    url = f"{BASEAPI}/risk-regime-live"
    params = {"risk": risk}

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return response["data"]
