"""
Tests for tickers API endpoint.
"""

from unravel_client import get_tickers


def test_get_tickers_success(api_key, test_portfolio_base):
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
