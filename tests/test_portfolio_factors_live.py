"""
Tests for portfolio factors live API endpoint.
"""
import pandas as pd
from unravel_client import get_portfolio_factors_live, get_tickers


def test_get_portfolio_factors_live_success(
    api_key, test_portfolio, test_portfolio_base
):
    """Test successful retrieval of live factors."""
    # First get some tickers to use
    tickers = get_tickers(
        id=test_portfolio_base,
        api_key=api_key,
        universe_size=20,
    )

    if len(tickers) > 0:
        result = get_portfolio_factors_live(
            id=test_portfolio,
            tickers=tickers[:3],
            api_key=api_key,
        )

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) > 0, "Should have some live factor data"
        assert len(result) <= 3, "Should have data for the tickers we requested"
        assert pd.api.types.is_float_dtype(result), "Values should be float type"


def test_get_portfolio_factors_live_with_smoothing(
    api_key, test_portfolio, test_portfolio_base
):
    """Test live factors with smoothing parameter."""
    # First get some tickers to use
    tickers = get_tickers(
        id=test_portfolio_base,
        api_key=api_key,
        universe_size=20,
    )

    if len(tickers) > 0:
        result = get_portfolio_factors_live(
            id=test_portfolio,
            tickers=tickers[:2],
            api_key=api_key,
            smoothing="5",
        )

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) > 0, "Should have some live factor data"
        assert pd.api.types.is_float_dtype(result), "Values should be float type"


def test_as_of_close_vs_latest_differ(api_key, test_portfolio, test_portfolio_base):
    """Test that as_of='close' and as_of='latest' return different results."""
    tickers = get_tickers(
        id=test_portfolio_base,
        api_key=api_key,
        universe_size=20,
    )

    if len(tickers) > 0:
        result_close = get_portfolio_factors_live(
            id=test_portfolio,
            tickers=tickers[:3],
            api_key=api_key,
            as_of="close",
        )
        result_latest = get_portfolio_factors_live(
            id=test_portfolio,
            tickers=tickers[:3],
            api_key=api_key,
            as_of="latest",
        )

        assert not result_close.equals(result_latest), (
            "as_of='close' and as_of='latest' should return different factor values"
        )
