"""
Tests for portfolio historical weights API endpoint.
"""
from datetime import datetime, timedelta

import pandas as pd
import pytest
import requests
from unravel_client import get_portfolio_historical_weights


def test_get_portfolio_historical_weights_success(api_key, test_portfolio):
    """Test successful retrieval of historical portfolio weights."""
    # Use a recent date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    result = get_portfolio_historical_weights(
        portfolio=test_portfolio,
        api_key=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Assertions
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0, "Should have some historical data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert all(
        isinstance(col, str) for col in result.columns
    ), "Columns should be strings"


def test_dataframe_dtypes(api_key, test_portfolio):
    """Test that DataFrame columns are properly converted to float."""
    # Use a recent date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    result = get_portfolio_historical_weights(
        portfolio=test_portfolio,
        api_key=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Check that all columns are float type
    for col in result.columns:
        assert pd.api.types.is_float_dtype(result[col])


def test_date_range_handling(api_key, test_portfolio):
    """Test that date ranges are handled correctly."""
    # Test with different date formats
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    result = get_portfolio_historical_weights(
        portfolio=test_portfolio,
        api_key=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Should have data within the specified range
    assert len(result) > 0
    assert result.index.min() >= pd.to_datetime(start_date)
    assert result.index.max() <= pd.to_datetime(end_date)


def test_invalid_portfolio_error(api_key):
    """Test error handling for invalid portfolio."""
    with pytest.raises(requests.HTTPError):
        get_portfolio_historical_weights(
            portfolio="invalid-portfolio-id",
            api_key=api_key,
        )


def test_invalid_api_key_error():
    """Test error handling for invalid API key."""
    with pytest.raises(requests.HTTPError):
        get_portfolio_historical_weights(
            portfolio="test-portfolio",
            api_key="invalid-api-key",
        )
