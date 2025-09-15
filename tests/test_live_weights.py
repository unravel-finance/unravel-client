"""
Tests for live weights API endpoint.
"""
import pandas as pd
from unravel_client import get_live_weights


class TestLiveWeights:
    """Test live weights API function."""

    def test_get_live_weights_success(self, api_key, test_portfolio):
        """Test successful retrieval of live portfolio weights."""
        result = get_live_weights(portfolio=test_portfolio, API_KEY=api_key)

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) > 0, "Should have some live weights"
        assert all(
            isinstance(idx, str) for idx in result.index
        ), "Index should be strings"
        assert pd.api.types.is_float_dtype(result), "Values should be float type"

    def test_series_dtypes(self, api_key, test_portfolio):
        """Test that Series values are properly converted to float."""
        result = get_live_weights(portfolio=test_portfolio, API_KEY=api_key)

        # Check that all values are float type
        assert pd.api.types.is_float_dtype(result)
