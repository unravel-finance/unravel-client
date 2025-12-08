<img width="1584" height="396" alt="github-cover" src="https://github.com/user-attachments/assets/ede1334b-571c-4f64-a6c3-465138a15526" />

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
api_key = "your-api-key-here"

# Get historical portfolio weights
historical_weights = unravel_client.get_portfolio_historical_weights(
    id="your-portfolio-id",
    api_key=api_key,
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# Get current portfolio weights
live_weights = unravel_client.get_live_weights(
    id="your-portfolio-id",
    api_key=api_key
)


# Get portfolio returns
returns = unravel_client.get_portfolio_returns(
    id="your-portfolio-id",
    api_key=api_key,
    start_date="2024-01-01"
)

# Get portfolio tickers
tickers = unravel_client.get_tickers(
    id="momentum",  # Portfolio factor identifier without universe specifier
    api_key=api_key,
    universe_size="full"
)

# Get historical factors
factors = unravel_client.get_portfolio_factors_historical(
    id="momentum",  # Portfolio factor identifier without universe specifier
    tickers=["BTC", "ETH"],
    api_key=api_key
)

# Get live factors (latest factor data)
live_factors = unravel_client.get_portfolio_factors_live(
    id="momentum",
    tickers=["BTC", "ETH"],
    api_key=api_key
)

# Get price data (deprecated endpoint)
price = unravel_client.get_price(
    ticker="BTC",
    api_key=api_key,
    start_date="2024-01-01"
)

# Get historical universe
universe = unravel_client.get_historical_universe(
    size="full",
    start_date="2024-01-01",
    end_date="2024-12-31",
    api_key=api_key
)
```

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
- **Cross-Sectional Factors**: Tests factor API calls
- **Error Handling**: Tests error handling for invalid requests
- **Data Types**: Tests data type conversion and validation

### CI/CD

The GitHub Actions workflow automatically runs tests using secrets:

- `UNRAVEL_API_KEY`: Your API key

## Support

For issues and questions, please visit our [GitHub repository](https://github.com/unravel-finance/unravel-client/issues).
