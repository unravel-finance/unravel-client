"""
Tests for universe API endpoint.
"""

import pandas as pd
import pytest
from unravel_client import get_historical_universe


def test_get_historical_universe_success(api_key):
    """Test successful retrieval of historical universe."""
    result = get_historical_universe(
        size="full",
        start_date="2024-01-01",
        end_date="2024-01-31",
        API_KEY=api_key,
    )

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0, "Should have some data"
    assert len(result.columns) > 0, "Should have some tickers"
    assert len(result.index) > 0, "Should have some dates"

    # Check that all values are boolean (True/False)
    assert result.dtypes.apply(
        lambda x: x == bool
    ).all(), "All values should be boolean"

    # Check that index is datetime
    assert isinstance(result.index, pd.DatetimeIndex), "Index should be DatetimeIndex"


def test_get_historical_universe_different_sizes(api_key):
    """Test historical universe with different size parameters."""
    sizes = ["full", "50", "100"]

    for size in sizes:
        result = get_historical_universe(
            size=size,
            start_date="2024-01-01",
            end_date="2024-01-07",
            API_KEY=api_key,
        )

        # Basic assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0, f"Should have some data for size {size}"
        assert len(result.columns) > 0, f"Should have some tickers for size {size}"
        assert len(result.index) > 0, f"Should have some dates for size {size}"


def test_get_historical_universe_date_range(api_key):
    """Test historical universe with different date ranges."""
    date_ranges = [
        ("2024-01-01", "2024-01-07"),  # 1 week
        ("2024-01-01", "2024-01-31"),  # 1 month
        ("2024-01-01", "2024-03-31"),  # 3 months
    ]

    for start_date, end_date in date_ranges:
        result = get_historical_universe(
            size="full",
            start_date=start_date,
            end_date=end_date,
            API_KEY=api_key,
        )

        # Basic assertions
        assert isinstance(result, pd.DataFrame)
        assert (
            len(result) > 0
        ), f"Should have some data for range {start_date} to {end_date}"
        assert (
            len(result.columns) > 0
        ), f"Should have some tickers for range {start_date} to {end_date}"
        assert (
            len(result.index) > 0
        ), f"Should have some dates for range {start_date} to {end_date}"

        # Check that the date range is reasonable
        assert result.index.min() >= pd.to_datetime(
            start_date
        ), f"Start date should be >= {start_date}"
        assert result.index.max() <= pd.to_datetime(
            end_date
        ), f"End date should be <= {end_date}"


def test_get_historical_universe_invalid_parameters(api_key):
    """Test historical universe with invalid parameters."""
    # Test with invalid size
    with pytest.raises(AssertionError):
        get_historical_universe(
            size="invalid_size",
            start_date="2024-01-01",
            end_date="2024-01-31",
            API_KEY=api_key,
        )

    # Test with invalid date format
    with pytest.raises(AssertionError):
        get_historical_universe(
            size="full",
            start_date="invalid-date",
            end_date="2024-01-31",
            API_KEY=api_key,
        )

    # Test with invalid API key
    with pytest.raises(AssertionError):
        get_historical_universe(
            size="full",
            start_date="2024-01-01",
            end_date="2024-01-31",
            API_KEY="invalid_key",
        )


def test_get_historical_universe_data_consistency(api_key):
    """Test that historical universe data is consistent."""
    result = get_historical_universe(
        size="full",
        start_date="2024-01-01",
        end_date="2024-01-31",
        API_KEY=api_key,
    )

    # Check that we have consistent data structure
    assert isinstance(result, pd.DataFrame)

    # Check that all ticker columns are strings
    assert all(
        isinstance(col, str) for col in result.columns
    ), "All column names should be strings"

    # Check that ticker names look reasonable (uppercase, reasonable length)
    for col in result.columns:
        assert col.isupper(), f"Ticker {col} should be uppercase"
        assert 2 <= len(col) <= 10, f"Ticker {col} should have reasonable length"

    # Check that dates are in chronological order
    assert (
        result.index.is_monotonic_increasing
    ), "Dates should be in chronological order"
