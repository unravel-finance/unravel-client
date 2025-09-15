# Unravel Client

A Python client library for accessing the Unravel Finance API, providing convenient wrappers for multi-factor, market-neutral crypto portfolio data and risk signals.

## Installation

```bash
pip install unravel-client
```

## Features

- **Portfolio Data**: Access historical and live portfolio weights
- **Cross-section Factors**: Access cross-sectional factors as raw data
- **Risk Signals**: Retrieve normalized risk factor series for cryptocurrencies
- **Easy Integration**: Simple API calls with pandas DataFrame/Series returns

## Quick Start

```python
import unravel_client

# Set your API key
API_KEY = "your-api-key-here"

# Get historical portfolio weights
historical_weights = unravel_client.get_portfolio_historical_weights(
    portfolio="your-portfolio-id",
    API_KEY=API_KEY,
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# Get current portfolio weights
live_weights = unravel_client.get_live_weights(
    portfolio="your-portfolio-id",
    API_KEY=API_KEY
)

# Get normalized risk signals
risk_signal = unravel_client.get_normalized_series(
    ticker="BTC",
    series="meta_risk",
    API_KEY=API_KEY,
    start_date="2024-01-01"
)

# Get portfolio returns
returns = unravel_client.get_portfolio_returns(
    portfolioId="your-portfolio-id",
    API_KEY=API_KEY,
    start_date="2024-01-01"
)

# Get portfolio tickers
tickers = unravel_client.get_tickers(
    portfolioId="your-portfolio-id",
    API_KEY=API_KEY,
    universe_size="full"
)

# Get historical factors
factors = unravel_client.get_portfolio_factors_historical(
    portfolioId="your-portfolio-id",
    tickers=["BTC", "ETH"],
    API_KEY=API_KEY
)
```

## API Reference

### Portfolio Functions

#### `get_portfolio_historical_weights(portfolio, API_KEY, start_date=None, end_date=None, smoothing=None)`

Fetch historical portfolio weights from the Unravel API.

**Parameters:**

- `portfolio` (str): The portfolio ID
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Start date in 'YYYY-MM-DD' format
- `end_date` (str, optional): End date in 'YYYY-MM-DD' format
- `smoothing` (str, optional): Smoothing parameter

**Returns:** `pandas.DataFrame` with historical weights

#### `get_live_weights(portfolio, API_KEY)`

Fetch current portfolio weights from the Unravel API.

**Parameters:**

- `portfolio` (str): The portfolio ID
- `API_KEY` (str): Your API key

**Returns:** `pandas.Series` with current weights

#### `get_portfolio_returns(portfolioId, API_KEY, start_date=None, end_date=None, smoothing=None)`

Fetch portfolio returns from the Unravel API.

**Parameters:**

- `portfolioId` (str): The portfolio ID
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Start date in 'YYYY-MM-DD' format
- `end_date` (str, optional): End date in 'YYYY-MM-DD' format
- `smoothing` (str, optional): Smoothing parameter

**Returns:** `pandas.Series` with portfolio returns

#### `get_tickers(portfolioId, API_KEY, universe_size)`

Fetch the tickers for a portfolio from the Unravel API.

**Parameters:**

- `portfolioId` (str): The portfolio ID
- `API_KEY` (str): Your API key
- `universe_size` (int | str): Universe size or 'full' for all available tickers

**Returns:** `list[str]` with ticker symbols

#### `get_portfolio_factors_historical(portfolioId, tickers, API_KEY)`

Fetch historical factors for a portfolio from the Unravel API.

**Parameters:**

- `portfolioId` (str): The portfolio ID
- `tickers` (list[str]): List of tickers in the portfolio
- `API_KEY` (str): Your API key

**Returns:** `pandas.DataFrame` with historical factor data

### Risk Signal Functions

#### `get_normalized_series(ticker, series, API_KEY, start_date=None, end_date=None, smoothing=None)`

Fetch normalized risk signal data from the Unravel API.

**Parameters:**

- `ticker` (str): Cryptocurrency ticker symbol (e.g., 'BTC', 'ETH')
- `series` (str): Risk factor series (e.g., 'meta_risk')
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Start date in 'YYYY-MM-DD' format
- `end_date` (str, optional): End date in 'YYYY-MM-DD' format
- `smoothing` (int, optional): Smoothing window

**Returns:** `pandas.Series` with risk signal data

## Requirements

- Python 3.11+
- pandas >= 2.0.0
- numpy >= 1.3.0
- requests >= 2.25.0
- tqdm >= 4.66.4

## License

MIT License

## Authors

[Unravel Finance](https://unravel.finance)

## Testing

The test suite uses real API endpoints to ensure the library works correctly with the actual Unravel API.

### Setting up Environment Variables

You need to set up environment variables for testing:

```bash
# Required: Your Unravel API key
export UNRAVEL_API_KEY="your_api_key_here"
```

### Running Tests

```bash
# Install with test dependencies
pip install -e ".[tests]"

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_unravel_client.py::TestRiskSignalFunctions -v
pytest tests/test_unravel_client.py::TestErrorHandling -v
```

### Test Categories

- **Portfolio Functions**: Tests portfolio-related API calls using `momentum_enhanced.40` portfolio
- **Risk Signal Functions**: Tests risk signal API calls
- **Error Handling**: Tests error handling for invalid requests
- **Data Types**: Tests data type conversion and validation

### CI/CD

The GitHub Actions workflow automatically runs tests using secrets:

- `UNRAVEL_API_KEY`: Your API key

## Support

For issues and questions, please visit our [GitHub repository](https://github.com/unravel-finance/unravel-client/issues).
