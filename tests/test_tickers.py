"""
Tests for tickers API endpoint.
"""

from unravel_client import get_tickers


class TestTickers:
    """Test tickers API function."""

    def test_get_tickers_success(self, api_key, test_portfolio):
        """Test successful retrieval of portfolio tickers."""
        result = get_tickers(
            portfolioId=test_portfolio,
            API_KEY=api_key,
            universe_size="full",
        )

        # Assertions
        assert isinstance(result, list)
        assert len(result) > 0, "Should have some tickers"
        assert all(
            isinstance(ticker, str) for ticker in result
        ), "All tickers should be strings"
