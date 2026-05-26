"""
Tests that live* endpoints return different values for as_of="latest" vs as_of="close".
"""
import pandas as pd
import pytest

from unravel_client import (
    get_live_weights,
    get_portfolio_factors_live,
    get_risk_overlay_live,
    get_risk_regime_live,
    get_tickers,
)


def test_live_weights_latest_vs_close_differ(api_key, test_portfolio):
    """Passing as_of='latest' and as_of='close' should return different weight values."""
    result_latest = get_live_weights(id=test_portfolio, api_key=api_key, as_of="latest")
    result_close = get_live_weights(id=test_portfolio, api_key=api_key, as_of="close")

    assert isinstance(result_latest, pd.Series)
    assert isinstance(result_close, pd.Series)
    assert len(result_latest) > 0
    assert len(result_close) > 0

    # The two snapshots should not be identical
    assert not result_latest.equals(result_close), (
        "as_of='latest' and as_of='close' returned identical weights — "
        "expected them to differ because intraday prices differ from the previous close"
    )


def test_portfolio_factors_live_latest_vs_close_differ(
    api_key, test_portfolio, test_portfolio_base
):
    """Passing as_of='latest' and as_of='close' should return different factor values."""
    tickers = get_tickers(id=test_portfolio_base, api_key=api_key, universe_size=20)
    if len(tickers) == 0:
        pytest.skip("No tickers available for this portfolio")

    sample = tickers[:3]
    result_latest = get_portfolio_factors_live(
        id=test_portfolio, tickers=sample, api_key=api_key, as_of="latest"
    )
    result_close = get_portfolio_factors_live(
        id=test_portfolio, tickers=sample, api_key=api_key, as_of="close"
    )

    assert isinstance(result_latest, pd.Series)
    assert isinstance(result_close, pd.Series)
    assert len(result_latest) > 0
    assert len(result_close) > 0

    assert not result_latest.equals(result_close), (
        "as_of='latest' and as_of='close' returned identical factor values — "
        "expected them to differ because intraday prices differ from the previous close"
    )


def test_risk_overlay_live_latest_vs_close_differ(api_key, test_portfolio_base):
    """Passing as_of='latest' and as_of='close' should return different overlay values."""
    result_latest = get_risk_overlay_live(
        portfolio=test_portfolio_base, overlay="trend", api_key=api_key, as_of="latest"
    )
    result_close = get_risk_overlay_live(
        portfolio=test_portfolio_base, overlay="trend", api_key=api_key, as_of="close"
    )

    assert isinstance(result_latest, pd.Series)
    assert isinstance(result_close, pd.Series)
    assert len(result_latest) == 1
    assert len(result_close) == 1

    assert not result_latest.equals(result_close), (
        "as_of='latest' and as_of='close' returned identical risk overlay values — "
        "expected them to differ because intraday prices differ from the previous close"
    )


def test_risk_regime_live_latest_vs_close_differ(api_key):
    """Passing as_of='latest' and as_of='close' should return different regime values."""
    result_latest = get_risk_regime_live(
        overlay="crypto_trend_consensus", api_key=api_key, as_of="latest"
    )
    result_close = get_risk_regime_live(
        overlay="crypto_trend_consensus", api_key=api_key, as_of="close"
    )

    assert isinstance(result_latest, pd.Series)
    assert isinstance(result_close, pd.Series)
    assert len(result_latest) == 1
    assert len(result_close) == 1

    assert not result_latest.equals(result_close), (
        "as_of='latest' and as_of='close' returned identical risk regime values — "
        "expected them to differ because intraday prices differ from the previous close"
    )
