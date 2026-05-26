"""
Tests for live weights API endpoint.
"""
import pandas as pd
from unravel_client import get_live_weights


def test_get_live_weights_success(api_key, test_portfolio):
    """Test successful retrieval of live portfolio weights."""
    result = get_live_weights(id=test_portfolio, api_key=api_key)

    # Assertions
    assert isinstance(result, pd.Series)
    assert len(result) > 0, "Should have some live weights"
    assert all(isinstance(idx, str) for idx in result.index), "Index should be strings"
    assert pd.api.types.is_float_dtype(result), "Values should be float type"


def test_series_dtypes(api_key, test_portfolio):
    """Test that Series values are properly converted to float."""
    result = get_live_weights(id=test_portfolio, api_key=api_key)

    # Check that all values are float type
    assert pd.api.types.is_float_dtype(result)


def test_as_of_close_vs_latest_differ(api_key, test_portfolio):
    """Test that as_of='close' and as_of='latest' return different results."""
    result_close = get_live_weights(id=test_portfolio, api_key=api_key, as_of="close")
    result_latest = get_live_weights(id=test_portfolio, api_key=api_key, as_of="latest")

    assert not result_close.equals(result_latest), (
        "as_of='close' and as_of='latest' should return different weights"
    )
