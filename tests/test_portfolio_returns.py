"""
Tests for portfolio returns API endpoint.
"""

import pandas as pd
from unravel_client import get_portfolio_returns


def test_get_portfolio_returns_success(api_key, test_portfolio):
    """Test successful retrieval of portfolio returns."""
    # Use a recent date range
    # end_date = datetime.now().strftime("%Y-%m-%d")
    # start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    result = get_portfolio_returns(
        portfolio=test_portfolio,
        api_key=api_key,
        # start_date=start_date,
        # end_date=end_date,
    )

    # Assertions
    assert isinstance(result, pd.Series)
    assert len(result) > 0, "Should have some return data"
    assert isinstance(result.index, pd.DatetimeIndex)
    assert pd.api.types.is_float_dtype(result), "Values should be float type"
