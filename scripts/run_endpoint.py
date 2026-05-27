from __future__ import annotations

import argparse
import json
import os
from datetime import date, timedelta
from typing import Any, Callable

import pandas as pd

from unravel_client import (
    get_historical_universe,
    get_live_weights,
    get_portfolio_factors_historical,
    get_portfolio_factors_live,
    get_portfolio_historical_weights,
    get_portfolio_returns,
    get_price,
    get_prices,
    get_risk_overlay,
    get_risk_overlay_live,
    get_risk_regime,
    get_risk_regime_live,
    get_tickers,
)

DEFAULT_PORTFOLIO = "momentum_enhanced.40"
DEFAULT_PORTFOLIO_BASE = "momentum_enhanced"
DEFAULT_OVERLAY = "trend"
DEFAULT_REGIME_OVERLAY = "crypto_trend_consensus"

EndpointDefaultsFactory = Callable[[str], dict[str, Any]]
EndpointCallable = Callable[..., Any]


def recent_date_range(days: int = 30) -> tuple[str, str]:
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return start_date.isoformat(), end_date.isoformat()


def sample_factor_tickers(api_key: str, count: int = 3) -> list[str]:
    tickers = get_tickers(
        id=DEFAULT_PORTFOLIO_BASE,
        api_key=api_key,
        universe_size=20,
    )
    if not tickers:
        msg = "No sample tickers were returned for the default portfolio."
        raise RuntimeError(msg)
    return tickers[:count]


def defaults_for_get_price(_: str) -> dict[str, Any]:
    start_date, end_date = recent_date_range()
    return {
        "ticker": "BTC",
        "start_date": start_date,
        "end_date": end_date,
    }


def defaults_for_get_prices(_: str) -> dict[str, Any]:
    start_date, end_date = recent_date_range()
    return {
        "tickers": ["BTC", "ETH"],
        "start_date": start_date,
        "end_date": end_date,
    }


def defaults_for_historical_weights(_: str) -> dict[str, Any]:
    start_date, end_date = recent_date_range()
    return {
        "id": DEFAULT_PORTFOLIO,
        "start_date": start_date,
        "end_date": end_date,
    }


def defaults_for_live_weights(_: str) -> dict[str, Any]:
    return {"id": DEFAULT_PORTFOLIO}


def defaults_for_returns(_: str) -> dict[str, Any]:
    start_date, end_date = recent_date_range()
    return {
        "id": DEFAULT_PORTFOLIO,
        "start_date": start_date,
        "end_date": end_date,
    }


def defaults_for_tickers(_: str) -> dict[str, Any]:
    return {
        "id": DEFAULT_PORTFOLIO_BASE,
        "universe_size": "full",
    }


def defaults_for_factors_historical(api_key: str) -> dict[str, Any]:
    start_date, end_date = recent_date_range()
    return {
        "id": DEFAULT_PORTFOLIO,
        "tickers": sample_factor_tickers(api_key),
        "start_date": start_date,
        "end_date": end_date,
    }


def defaults_for_factors_live(api_key: str) -> dict[str, Any]:
    return {
        "id": DEFAULT_PORTFOLIO,
        "tickers": sample_factor_tickers(api_key),
    }


def defaults_for_risk_overlay(_: str) -> dict[str, Any]:
    start_date, end_date = recent_date_range()
    return {
        "portfolio": DEFAULT_PORTFOLIO_BASE,
        "overlay": DEFAULT_OVERLAY,
        "start_date": start_date,
        "end_date": end_date,
    }


def defaults_for_risk_overlay_live(_: str) -> dict[str, Any]:
    return {
        "portfolio": DEFAULT_PORTFOLIO_BASE,
        "overlay": DEFAULT_OVERLAY,
    }


def defaults_for_risk_regime(_: str) -> dict[str, Any]:
    return {
        "overlay": DEFAULT_REGIME_OVERLAY,
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
    }


def defaults_for_risk_regime_live(_: str) -> dict[str, Any]:
    return {"overlay": DEFAULT_REGIME_OVERLAY}


def defaults_for_historical_universe(_: str) -> dict[str, Any]:
    return {
        "size": "20",
        "start_date": "2024-01-01",
        "end_date": "2024-01-07",
    }


ENDPOINTS: dict[str, tuple[EndpointCallable, EndpointDefaultsFactory]] = {
    "get_historical_universe": (get_historical_universe, defaults_for_historical_universe),
    "get_live_weights": (get_live_weights, defaults_for_live_weights),
    "get_portfolio_factors_historical": (
        get_portfolio_factors_historical,
        defaults_for_factors_historical,
    ),
    "get_portfolio_factors_live": (
        get_portfolio_factors_live,
        defaults_for_factors_live,
    ),
    "get_portfolio_historical_weights": (
        get_portfolio_historical_weights,
        defaults_for_historical_weights,
    ),
    "get_portfolio_returns": (get_portfolio_returns, defaults_for_returns),
    "get_price": (get_price, defaults_for_get_price),
    "get_prices": (get_prices, defaults_for_get_prices),
    "get_risk_overlay": (get_risk_overlay, defaults_for_risk_overlay),
    "get_risk_overlay_live": (get_risk_overlay_live, defaults_for_risk_overlay_live),
    "get_risk_regime": (get_risk_regime, defaults_for_risk_regime),
    "get_risk_regime_live": (get_risk_regime_live, defaults_for_risk_regime_live),
    "get_tickers": (get_tickers, defaults_for_tickers),
}


def parse_overrides(raw_overrides: str) -> dict[str, Any]:
    if not raw_overrides.strip():
        return {}

    overrides = json.loads(raw_overrides)
    if not isinstance(overrides, dict):
        msg = "--overrides must be a JSON object."
        raise ValueError(msg)
    return overrides


def print_result(result: Any) -> None:
    print("\nResult summary:")

    if isinstance(result, pd.DataFrame):
        print(f"type=DataFrame shape={result.shape}")
        print(result.head().to_string())
        return

    if isinstance(result, pd.Series):
        print(f"type=Series length={len(result)}")
        print(result.head().to_string())
        return

    if isinstance(result, list):
        print(f"type=list length={len(result)}")
        print(json.dumps(result[:10], indent=2))
        return

    print(repr(result))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a sample call for any exported unravel_client endpoint.",
    )
    parser.add_argument(
        "--endpoint",
        choices=sorted(ENDPOINTS),
        required=True,
        help="Endpoint function to execute.",
    )
    parser.add_argument(
        "--overrides",
        default="",
        help='JSON object merged into the default sample kwargs, e.g. {"as_of":"latest"}.',
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    api_key = os.getenv("UNRAVEL_API_KEY")
    if not api_key:
        msg = "UNRAVEL_API_KEY is required. Put it in .env or your environment before launching."
        raise SystemExit(msg)

    endpoint, defaults_factory = ENDPOINTS[args.endpoint]
    kwargs = defaults_factory(api_key)
    kwargs.update(parse_overrides(args.overrides))

    print(f"Calling {args.endpoint}")
    print(json.dumps(kwargs, indent=2, sort_keys=True, default=str))

    result = endpoint(api_key=api_key, **kwargs)
    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
