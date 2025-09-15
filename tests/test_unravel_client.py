"""
Tests for unravel-client API functions.
"""
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from unravel_client import (
    get_live_weights,
    get_normalized_series,
    get_portfolio_historical_weights,
)


class TestPortfolioFunctions:
    """Test portfolio-related API functions."""

    @patch("unravel_client.portfolio.historical_weights.requests.get")
    def test_get_portfolio_historical_weights_success(self, mock_get):
        """Test successful retrieval of historical portfolio weights."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [[0.5, 0.3, 0.2], [0.6, 0.25, 0.15]],
            "index": ["2024-01-01", "2024-01-02"],
            "columns": ["BTC", "ETH", "SOL"],
        }
        mock_get.return_value = mock_response

        # Test function
        result = get_portfolio_historical_weights(
            portfolio="test-portfolio",
            API_KEY="test-key",
            start_date="2024-01-01",
            end_date="2024-01-02",
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (2, 3)
        assert list(result.columns) == ["BTC", "ETH", "SOL"]
        assert isinstance(result.index, pd.DatetimeIndex)

        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "portfolio/historical-weights" in call_args[0][0]
        assert call_args[1]["headers"]["X-API-KEY"] == "test-key"
        assert call_args[1]["params"]["portfolio"] == "test-portfolio"

    @patch("unravel_client.portfolio.historical_weights.requests.get")
    def test_get_portfolio_historical_weights_error(self, mock_get):
        """Test error handling for historical portfolio weights."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid portfolio"}
        mock_get.return_value = mock_response

        # Test that assertion is raised
        with pytest.raises(AssertionError):
            get_portfolio_historical_weights(
                portfolio="invalid-portfolio", API_KEY="test-key"
            )

    @patch("unravel_client.portfolio.live_weights.requests.get")
    def test_get_live_weights_success(self, mock_get):
        """Test successful retrieval of live portfolio weights."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [0.5, 0.3, 0.2],
            "columns": ["BTC", "ETH", "SOL"],
            "index": "portfolio_weights",
        }
        mock_get.return_value = mock_response

        # Test function
        result = get_live_weights(portfolio="test-portfolio", API_KEY="test-key")

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert list(result.index) == ["BTC", "ETH", "SOL"]
        assert result.name == "portfolio_weights"

        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "portfolio/live-weights" in call_args[0][0]
        assert call_args[1]["headers"]["X-API-KEY"] == "test-key"
        assert call_args[1]["params"]["portfolio"] == "test-portfolio"


class TestRiskSignalFunctions:
    """Test risk signal API functions."""

    @patch("unravel_client.factor.normalized_series.requests.get")
    def test_get_normalized_series_success(self, mock_get):
        """Test successful retrieval of normalized risk series."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [0.1, 0.2, 0.15, 0.3],
            "index": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        }
        mock_get.return_value = mock_response

        # Test function
        result = get_normalized_series(
            ticker="BTC",
            series="meta_risk",
            API_KEY="test-key",
            start_date="2024-01-01",
            end_date="2024-01-04",
        )

        # Assertions
        assert isinstance(result, pd.Series)
        assert len(result) == 4
        assert result.name == "BTC"
        assert isinstance(result.index, pd.DatetimeIndex)

        # Verify API call
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "normalized-series" in call_args[0][0]
        assert call_args[1]["headers"]["X-API-KEY"] == "test-key"
        assert call_args[1]["params"]["ticker"] == "BTC"
        assert call_args[1]["params"]["series"] == "meta_risk"

    @patch("unravel_client.factor.normalized_series.requests.get")
    def test_get_normalized_series_error(self, mock_get):
        """Test error handling for normalized series."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Series not found"}
        mock_get.return_value = mock_response

        # Test that assertion is raised
        with pytest.raises(AssertionError):
            get_normalized_series(
                ticker="INVALID", series="meta_risk", API_KEY="test-key"
            )


class TestDataTypes:
    """Test data type handling and edge cases."""

    @patch("unravel_client.portfolio.historical_weights.requests.get")
    def test_dataframe_dtypes(self, mock_get):
        """Test that DataFrame columns are properly converted to float."""
        # Mock response with string numbers
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [["0.5", "0.3"], ["0.6", "0.4"]],
            "index": ["2024-01-01", "2024-01-02"],
            "columns": ["BTC", "ETH"],
        }
        mock_get.return_value = mock_response

        result = get_portfolio_historical_weights(
            portfolio="test-portfolio", API_KEY="test-key"
        )

        # Check that all columns are float type
        for col in result.columns:
            assert pd.api.types.is_float_dtype(result[col])

    @patch("unravel_client.portfolio.live_weights.requests.get")
    def test_series_dtypes(self, mock_get):
        """Test that Series values are properly converted to float."""
        # Mock response with string numbers
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": ["0.5", "0.3", "0.2"],
            "columns": ["BTC", "ETH", "SOL"],
            "index": "portfolio_weights",
        }
        mock_get.return_value = mock_response

        result = get_live_weights(portfolio="test-portfolio", API_KEY="test-key")

        # Check that all values are float type
        assert pd.api.types.is_float_dtype(result)
