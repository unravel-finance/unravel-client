"""
Tests for risk API endpoints.
"""

import pandas as pd

from unravel_client import (
    get_risk_overlays,
    get_risk_overlays_live,
    get_risk_regime,
    get_risk_regime_live,
    get_tickers,
)


def test_get_risk_overlays_success(api_key, test_portfolio_base):
    """Test successful retrieval of risk overlays."""
    tickers = get_tickers(
        id=test_portfolio_base,
        api_key=api_key,
        universe_size=20,
    )

    if len(tickers) > 0:
        result = get_risk_overlays(
            portfolio=test_portfolio_base,
            risk="momentum",
            api_key=api_key,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0, "Should have risk overlay data"
        assert isinstance(result.index, pd.DatetimeIndex)
        assert result.shape[1] > 0, "Should have at least one column"

        for col in result.columns:
            assert pd.api.types.is_float_dtype(result[col]), (
                f"Column {col} should be float type"
            )


def test_get_risk_overlays_with_date_range(api_key, test_portfolio_base):
    """Test risk overlays with date filtering."""
    result = get_risk_overlays(
        portfolio=test_portfolio_base,
        risk="momentum",
        api_key=api_key,
        start_date="2023-01-01",
        end_date="2023-12-31",
    )

    if len(result) > 0:
        assert all(result.index >= pd.Timestamp("2023-01-01"))
        assert all(result.index <= pd.Timestamp("2023-12-31"))


def test_get_risk_overlays_live_success(api_key, test_portfolio_base):
    """Test successful retrieval of latest risk overlay."""
    result = get_risk_overlays_live(
        portfolio=test_portfolio_base,
        risk="momentum",
        api_key=api_key,
    )

    assert isinstance(result, (float | int | None))


def test_get_risk_regime_success(api_key):
    """Test successful retrieval of risk regime data."""
    result = get_risk_regime(
        risk="momentum",
        api_key=api_key,
    )

    assert isinstance(result, pd.Series)
    assert len(result) > 0, "Should have risk regime data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert pd.api.types.is_float_dtype(result), "Series values should be float type"


def test_get_risk_regime_with_date_range(api_key):
    """Test risk regime with date filtering."""
    result = get_risk_regime(
        risk="momentum",
        api_key=api_key,
        start_date="2023-01-01",
        end_date="2023-12-31",
    )

    if len(result) > 0:
        assert all(result.index >= pd.Timestamp("2023-01-01"))
        assert all(result.index <= pd.Timestamp("2023-12-31"))


def test_get_risk_regime_live_success(api_key):
    """Test successful retrieval of latest risk regime."""
    result = get_risk_regime_live(
        risk="momentum",
        api_key=api_key,
    )

    assert isinstance(result, (float | int | None))
