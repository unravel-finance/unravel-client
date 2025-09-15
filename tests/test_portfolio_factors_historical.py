"""
Tests for portfolio factors historical API endpoint.
"""
import pandas as pd
from unravel_client import get_portfolio_factors_historical, get_tickers


class TestPortfolioFactorsHistorical:
    """Test portfolio factors historical API function."""

    def test_get_portfolio_factors_historical_success(
        self, api_key, test_portfolio, test_portfolio_base
    ):
        """Test successful retrieval of historical factors."""
        # First get some tickers to use
        tickers = get_tickers(
            portfolioId=test_portfolio_base,
            API_KEY=api_key,
            universe_size=20,
        )

        if len(tickers) > 0:
            result = get_portfolio_factors_historical(
                portfolioId=test_portfolio,
                tickers=tickers[:3],
                API_KEY=api_key,
            )

            # Assertions
            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0, "Should have some factor data"
            assert isinstance(result.index, pd.DatetimeIndex)
            assert (
                len(result.columns) <= 3
            ), "Should have columns for the tickers we requested"
