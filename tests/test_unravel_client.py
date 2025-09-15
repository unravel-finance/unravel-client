"""
Tests for unravel-client API functions using real API endpoints.
"""
import os
from datetime import datetime, timedelta

import pandas as pd
import pytest

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars
from unravel_client import (
    get_live_weights,
    get_normalized_series,
    get_portfolio_factors_historical,
    get_portfolio_historical_weights,
    get_portfolio_returns,
    get_tickers,
)


@pytest.fixture(scope="session")
def api_key():
    """Get API key from environment variable."""
    api_key = os.getenv("UNRAVEL_API_KEY")
    if not api_key:
        pytest.skip("UNRAVEL_API_KEY environment variable not set")
    return api_key


@pytest.fixture(scope="session")
def test_portfolio():
    """Get test portfolio ID."""
    return "momentum_enhanced.40"


@pytest.fixture(scope="session")
def test_portfolio_base():
    """Get base portfolio ID for tickers API."""
    return "momentum_enhanced"


class TestPortfolioFunctions:
    """Test portfolio-related API functions."""

    def test_get_portfolio_historical_weights_success(self, api_key, test_portfolio):
        """Test successful retrieval of historical portfolio weights."""
        # Use a recent date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = get_portfolio_historical_weights(
            portfolio=test_portfolio,
            API_KEY=api_key,
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

    def test_get_portfolio_returns_success(self, api_key, test_portfolio):
        """Test successful retrieval of portfolio returns."""
        # Use a recent date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        result = get_portfolio_returns(
            portfolioId=test_portfolio,
            API_KEY=api_key,
            start_date=start_date,
            end_date=end_date,
        )

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) > 0, "Should have some return data"
        assert isinstance(result.index, pd.DatetimeIndex)
        assert pd.api.types.is_float_dtype(result), "Values should be float type"

    def test_get_tickers_success(self, api_key, test_portfolio_base):
        """Test successful retrieval of portfolio tickers."""
        result = get_tickers(
            portfolioId=test_portfolio_base,
            API_KEY=api_key,
            universe_size="full",
        )

        # Assertions
        assert isinstance(result, list)
        assert len(result) > 0, "Should have some tickers"
        assert all(
            isinstance(ticker, str) for ticker in result
        ), "All tickers should be strings"

    def test_get_portfolio_factors_historical_success(
        self, api_key, test_portfolio, test_portfolio_base
    ):
        """Test successful retrieval of historical factors."""
        # First get some tickers to use
        tickers = get_tickers(
            portfolioId=test_portfolio_base,
            API_KEY=api_key,
            universe_size=5,  # Get just a few tickers for testing
        )

        if len(tickers) > 0:
            result = get_portfolio_factors_historical(
                portfolioId=test_portfolio,
                tickers=tickers[:3],  # Use first 3 tickers
                API_KEY=api_key,
            )

            # Assertions
            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0, "Should have some factor data"
            assert isinstance(result.index, pd.DatetimeIndex)
            assert (
                len(result.columns) <= 3
            ), "Should have columns for the tickers we requested"


class TestRiskSignalFunctions:
    """Test risk signal API functions."""

    def test_get_normalized_series_success(self, api_key):
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


class TestErrorHandling:
    """Test error handling for invalid requests."""

    def test_invalid_portfolio_error(self, api_key):
        """Test error handling for invalid portfolio."""
        with pytest.raises(AssertionError):
            get_portfolio_historical_weights(
                portfolio="invalid-portfolio-id",
                API_KEY=api_key,
            )

    def test_invalid_ticker_error(self, api_key):
        """Test error handling for invalid ticker."""
        with pytest.raises(AssertionError):
            get_normalized_series(
                ticker="INVALID_TICKER",
                series="meta_risk",
                API_KEY=api_key,
            )

    def test_invalid_api_key_error(self):
        """Test error handling for invalid API key."""
        with pytest.raises(AssertionError):
            get_portfolio_historical_weights(
                portfolio="test-portfolio",
                API_KEY="invalid-api-key",
            )


class TestDataTypes:
    """Test data type handling and edge cases."""

    def test_dataframe_dtypes(self, api_key, test_portfolio):
        """Test that DataFrame columns are properly converted to float."""
        # Use a recent date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = get_portfolio_historical_weights(
            portfolio=test_portfolio,
            API_KEY=api_key,
            start_date=start_date,
            end_date=end_date,
        )

        # Check that all columns are float type
        for col in result.columns:
            assert pd.api.types.is_float_dtype(result[col])

    def test_series_dtypes(self, api_key, test_portfolio):
        """Test that Series values are properly converted to float."""
        result = get_live_weights(portfolio=test_portfolio, API_KEY=api_key)

        # Check that all values are float type
        assert pd.api.types.is_float_dtype(result)

    def test_date_range_handling(self, api_key, test_portfolio):
        """Test that date ranges are handled correctly."""
        # Test with different date formats
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        result = get_portfolio_historical_weights(
            portfolio=test_portfolio,
            API_KEY=api_key,
            start_date=start_date,
            end_date=end_date,
        )

        # Should have data within the specified range
        assert len(result) > 0
        assert result.index.min() >= pd.to_datetime(start_date)
        assert result.index.max() <= pd.to_datetime(end_date)
