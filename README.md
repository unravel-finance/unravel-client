# Unravel Client

A Python client library for accessing the Unravel Finance API, providing convenient wrappers for multi-factor, market-neutral crypto portfolio data and risk signals.

## Installation

```bash
pip install unravel-client
```

## Features

- **Portfolio Data**: Access historical and live portfolio weights
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
- requests

## License

MIT License

## Authors

[Unravel Finance](https://unravel.finance)

## Support

For issues and questions, please visit our [GitHub repository](https://github.com/unravel-finance/unravel-client/issues).
