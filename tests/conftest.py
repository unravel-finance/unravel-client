"""
Shared fixtures for unravel-client tests.
"""
import os

import pytest

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system env vars


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
