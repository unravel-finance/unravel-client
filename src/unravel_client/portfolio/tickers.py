import requests

from ..constants import BASEAPI
from ..decorators import retry_on_error


@retry_on_error(num_trials=3, wait=2.0)
def get_tickers(
    id: str,
    api_key: str,
    universe_size: int | str,
    exchange: str | None = None,
) -> list[str]:
    """
    Fetch the tickers for a portfolio from the Unravel API.

    Args:
        id (str): Portfolio Factor Identifier without the universe specifier (eg. momentum instead of momentum.20)
        api_key (str): The API key to use for the request
        universe_size (int | str): Universe size for the portfolio (e.g., 20, 30, 40) or 'full' to get all tickers.
        exchange (str | None): Exchange constraint for portfolio data. Valid options are found in the [Unravel Catalog](https://unravel.finance/home/api/catalog)

    Returns:
        list[str]: List of tickers in the portfolio
    """

    url = f"{BASEAPI}/portfolio/tickers"
    params = {"id": id, "universe_size": universe_size}

    if exchange is not None:
        params["exchange"] = exchange

    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return response["tickers"]
