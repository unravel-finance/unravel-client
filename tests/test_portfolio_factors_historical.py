"""
Tests for portfolio factors historical API endpoint.
"""
import pandas as pd
from unravel_client import get_portfolio_factors_historical, get_tickers


def test_get_portfolio_factors_historical_success(
    api_key, test_portfolio, test_portfolio_base
):
    """Test successful retrieval of historical factors."""
    # First get some tickers to use
    tickers = get_tickers(
        id=test_portfolio_base,
        api_key=api_key,
        universe_size=20,
    )

    if len(tickers) > 0:
        result = get_portfolio_factors_historical(
            id=test_portfolio,
            tickers=tickers[:3],
            api_key=api_key,
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0, "Should have some factor data"
        assert isinstance(result.index, pd.DatetimeIndex)
        assert (
            len(result.columns) <= 3
        ), "Should have columns for the tickers we requested"

        # Check dtypes for all columns
        for col in result.columns:
            assert pd.api.types.is_float_dtype(
                result[col]
            ), f"Column {col} should be float type"
