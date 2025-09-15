"""
Tests for normalized series API endpoint.
"""
from datetime import datetime, timedelta

import pandas as pd
import pytest
import requests
from unravel_client import get_normalized_series


def test_get_normalized_series_success(api_key):
    """Test successful retrieval of normalized risk series."""
    # Use a recent date range
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    result = get_normalized_series(
        ticker="BTC",
        series="meta_risk",
        API_KEY=api_key,
        start_date=start_date,
        end_date=end_date,
    )

    # Assertions
    assert isinstance(result, pd.Series)
    assert len(result) > 0, "Should have some risk signal data"
    assert result.name == "BTC"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert pd.api.types.is_float_dtype(result), "Values should be float type"


def test_invalid_ticker_error(api_key):
    """Test error handling for invalid ticker."""
    with pytest.raises(requests.HTTPError):
        get_normalized_series(
            ticker="INVALID_TICKER",
            series="meta_risk",
            API_KEY=api_key,
        )
