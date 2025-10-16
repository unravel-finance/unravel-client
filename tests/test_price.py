"""
Tests for price API endpoint.
"""
from datetime import datetime, timedelta

import pandas as pd
import requests
from unravel_client import get_price, get_prices


def test_get_price_success(api_key):
    """Test successful retrieval of price data."""
    # Use a recent date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    result = get_price(
        ticker="BTC",
        api_key=api_key,
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
        api_key=api_key,
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
            api_key=api_key,
        )

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) > 0, f"Should have some price data for {ticker}"
        assert isinstance(result.index, pd.DatetimeIndex)
        assert pd.api.types.is_float_dtype(
            result
        ), f"Values should be float type for {ticker}"


def test_get_prices_success(api_key):
    """Test successful retrieval of price data for multiple tickers."""
    # Use a recent date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    tickers = ["BTC", "ETH"]
    result = get_prices(
        tickers=tickers,
        api_key=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0, "Should have some price data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert len(result.columns) == len(
        tickers
    ), "Should have columns for all requested tickers"

    # Check that all columns are present
    for ticker in tickers:
        assert ticker in result.columns, f"Should have column for {ticker}"

    # Check dtypes for all columns
    for col in result.columns:
        assert pd.api.types.is_float_dtype(
            result[col]
        ), f"Column {col} should be float type"


def test_get_prices_without_date_range(api_key):
    """Test price retrieval for multiple tickers without date range."""
    tickers = ["BTC", "ETH", "SOL"]
    result = get_prices(
        tickers=tickers,
        api_key=api_key,
    )

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0, "Should have some price data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert len(result.columns) == len(
        tickers
    ), "Should have columns for all requested tickers"

    # Check that all columns are present
    for ticker in tickers:
        assert ticker in result.columns, f"Should have column for {ticker}"

    # Check dtypes for all columns
    for col in result.columns:
        assert pd.api.types.is_float_dtype(
            result[col]
        ), f"Column {col} should be float type"


def test_get_prices_single_ticker(api_key):
    """Test price retrieval for a single ticker using get_prices."""
    tickers = ["BTC"]
    result = get_prices(
        tickers=tickers,
        api_key=api_key,
    )

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0, "Should have some price data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert len(result.columns) == 1, "Should have one column for single ticker"
    assert "BTC" in result.columns, "Should have BTC column"
    assert pd.api.types.is_float_dtype(result["BTC"]), "BTC column should be float type"


def test_get_prices_multiple_tickers_different_sets(api_key):
    """Test price retrieval for different sets of tickers."""
    ticker_sets = [["BTC", "ETH"], ["SOL", "ADA"], ["BTC", "ETH", "SOL", "ADA"]]

    for tickers in ticker_sets:
        result = get_prices(
            tickers=tickers,
            api_key=api_key,
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0, f"Should have some price data for {tickers}"
        assert isinstance(result.index, pd.DatetimeIndex)
        assert len(result.columns) == len(
            tickers
        ), f"Should have columns for all requested tickers: {tickers}"

        # Check that all columns are present
        for ticker in tickers:
            assert ticker in result.columns, f"Should have column for {ticker}"

        # Check dtypes for all columns
        for col in result.columns:
            assert pd.api.types.is_float_dtype(
                result[col]
            ), f"Column {col} should be float type"


def test_get_prices_date_range_consistency(api_key):
    """Test that get_prices returns consistent date ranges."""
    tickers = ["BTC", "ETH"]
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    result = get_prices(
        tickers=tickers,
        api_key=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Check that the date range is reasonable
    assert result.index.min() >= pd.to_datetime(
        start_date
    ), f"Start date should be >= {start_date}"
    assert result.index.max() <= pd.to_datetime(
        end_date
    ), f"End date should be <= {end_date}"

    # Check that dates are in chronological order
    assert (
        result.index.is_monotonic_increasing
    ), "Dates should be in chronological order"

    # Check dtypes for all columns
    for col in result.columns:
        assert pd.api.types.is_float_dtype(
            result[col]
        ), f"Column {col} should be float type"


def test_get_prices_empty_tickers_list(api_key):
    """Test that get_prices handles empty tickers list appropriately."""
    # This should either raise an error or return an empty DataFrame
    # The behavior depends on the API implementation
    try:
        result = get_prices(
            tickers=[],
            api_key=api_key,
        )
        # If it doesn't raise an error, it should return an empty DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result.columns) == 0, "Should have no columns for empty tickers list"
    except (ValueError, requests.HTTPError):
        # If it raises an exception, that's also acceptable behavior
        pass
