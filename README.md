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
    portfolio="your-portfolio-id",
    API_KEY=API_KEY,
    start_date="2024-01-01"
)

# Get portfolio tickers
tickers = unravel_client.get_tickers(
    id="momentum",  # Portfolio factor identifier without universe specifier
    API_KEY=API_KEY,
    universe_size="full"
)

# Get historical factors
factors = unravel_client.get_portfolio_factors_historical(
    id="momentum",  # Portfolio factor identifier without universe specifier
    tickers=["BTC", "ETH"],
    API_KEY=API_KEY
)

# Get live factors (latest factor data)
live_factors = unravel_client.get_portfolio_factors_live(
    id="momentum",
    tickers=["BTC", "ETH"],
    API_KEY=API_KEY
)

# Get price data (deprecated endpoint)
price = unravel_client.get_price(
    ticker="BTC",
    API_KEY=API_KEY,
    start_date="2024-01-01"
)

# Get historical universe
universe = unravel_client.get_historical_universe(
    size="full",
    start_date="2024-01-01",
    end_date="2024-12-31",
    API_KEY=API_KEY
)
```

## API Reference

### Portfolio Functions

#### `get_portfolio_historical_weights(portfolio, API_KEY, start_date=None, end_date=None, smoothing=None, exchange=None)`

Fetch historical portfolio weights from the Unravel API.

**Parameters:**

- `portfolio` (str): Portfolio Identifier (eg. momentum.20)
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
- `end_date` (str, optional): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
- `smoothing` (str, optional): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
- `exchange` (str, optional): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.

**Returns:** `pandas.DataFrame` with historical weights

#### `get_live_weights(portfolio, API_KEY, smoothing=None, exchange=None)`

Fetch current portfolio weights from the Unravel API.

**Parameters:**

- `portfolio` (str): Portfolio Identifier (eg. momentum.20)
- `API_KEY` (str): Your API key
- `smoothing` (str, optional): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
- `exchange` (str, optional): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.

**Returns:** `pandas.Series` with current weights

#### `get_portfolio_returns(portfolio, API_KEY, start_date=None, end_date=None, smoothing=None, exchange=None)`

Fetch portfolio returns from the Unravel API.

**Parameters:**

- `portfolio` (str): Portfolio Identifier (eg. momentum.20)
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
- `end_date` (str, optional): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
- `smoothing` (str, optional): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
- `exchange` (str, optional): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.

**Returns:** `pandas.Series` with portfolio returns

#### `get_tickers(id, API_KEY, universe_size, exchange=None)`

Fetch the tickers for a portfolio from the Unravel API.

**Parameters:**

- `id` (str): Portfolio Factor Identifier without the universe specifier (eg. momentum instead of momentum.20)
- `API_KEY` (str): Your API key
- `universe_size` (int | str): Universe size for the portfolio (e.g., 20, 30, 40) or 'full' to get all tickers
- `exchange` (str, optional): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.

**Returns:** `list[str]` with ticker symbols

#### `get_portfolio_factors_historical(id, tickers, API_KEY, smoothing=None, start_date=None, end_date=None)`

Fetch historical factors for a portfolio from the Unravel API.

**Parameters:**

- `id` (str): Portfolio Factor Identifier without the universe specifier (eg. momentum instead of momentum.20)
- `tickers` (list[str]): List of tickers in the portfolio
- `API_KEY` (str): Your API key
- `smoothing` (str, optional): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.
- `start_date` (str, optional): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
- `end_date` (str, optional): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)

**Returns:** `pandas.DataFrame` with historical factor data

#### `get_portfolio_factors_live(id, tickers, API_KEY, smoothing=None)`

Fetch the latest factor data for specific tickers within a single factor portfolio.

**Parameters:**

- `id` (str): Portfolio Factor Identifier without the universe specifier (eg. momentum instead of momentum.20)
- `tickers` (list[str]): List of tickers in the portfolio
- `API_KEY` (str): Your API key
- `smoothing` (str, optional): Portfolio smoothing window for the data. Valid values are 0 (no smoothing), 5, 10, 15, 20, or 30 days.

**Returns:** `pandas.Series` with latest factor data

#### `get_historical_universe(size, start_date, end_date, API_KEY, exchange=None)`

Fetch the historical universe from the Unravel API.

**Parameters:**

- `size` (str): Portfolio size - number of assets to include. Must be one of: 20, 30, or 40
- `start_date` (str): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
- `end_date` (str): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
- `API_KEY` (str): Your API key
- `exchange` (str, optional): Exchange constraint for portfolio data. Valid options are: unconstrained (default), binance, okx, hyperliquid.

**Returns:** `pandas.DataFrame` with tickers in the portfolio [True and False]

### Risk Signal Functions

#### `get_normalized_series(ticker, series, API_KEY, start_date=None, end_date=None, smoothing=None)`

Fetch normalized risk signal data from the Unravel API.

**Parameters:**

- `ticker` (str): Ticker symbol (e.g., BTC, ETH)
- `series` (str): Series to retrieve (e.g., exchange_outflow, sentiment_aggregate)
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
- `end_date` (str, optional): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)
- `smoothing` (str, optional): Smoothing window for the data. Valid values are "default", "0", "7", "30". Default is "default".

**Returns:** `pandas.Series` with risk signal data

### Price Functions

#### `get_price(ticker, API_KEY, start_date=None, end_date=None)`

Fetch closing prices for a ticker from the Unravel API.

**Note:** This endpoint is deprecated and will only be used for technical integrations.

**Parameters:**

- `ticker` (str): Ticker symbol (e.g., BTC, ETH)
- `API_KEY` (str): Your API key
- `start_date` (str, optional): Filter data to only include dates on or after this date (ISO format: YYYY-MM-DD)
- `end_date` (str, optional): Filter data to only include dates on or before this date (ISO format: YYYY-MM-DD)

**Returns:** `pandas.Series` with closing prices

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
