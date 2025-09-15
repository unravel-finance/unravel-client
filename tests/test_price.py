"""
Tests for price API endpoint.
"""
from datetime import datetime, timedelta

import pandas as pd
from unravel_client import get_price


def test_get_price_success(api_key):
    """Test successful retrieval of price data."""
    # Use a recent date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    result = get_price(
        ticker="BTC",
        API_KEY=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Assertions
    assert isinstance(result, pd.Series)
    assert len(result) > 0, "Should have some price data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert pd.api.types.is_float_dtype(result), "Values should be float type"


def test_get_price_without_date_range(api_key):
    """Test price retrieval without date range."""
    result = get_price(
        ticker="BTC",
        API_KEY=api_key,
    )

    # Assertions
    assert isinstance(result, pd.Series)
    assert len(result) > 0, "Should have some price data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert pd.api.types.is_float_dtype(result), "Values should be float type"


def test_get_price_different_tickers(api_key):
    """Test price retrieval for different tickers."""
    tickers = ["BTC", "ETH", "SOL"]

    for ticker in tickers:
        result = get_price(
            ticker=ticker,
            API_KEY=api_key,
        )

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) > 0, f"Should have some price data for {ticker}"
        assert isinstance(result.index, pd.DatetimeIndex)
        assert pd.api.types.is_float_dtype(
            result
        ), f"Values should be float type for {ticker}"
