import requests

from ..constants import BASEAPI
from ..decorators import handle_api_errors


@handle_api_errors
def get_tickers(portfolioId: str, API_KEY: str, universe_size: int | str) -> list[str]:
    """
    Fetch the tickers for a portfolio from the Unravel API.

    Args:
        portfolioId (str): The portfolio ID
        API_KEY (str): The API key to use for the request
        universe_size (int | str): The universe size to use for the request.
            Pass in 'full' to get all available tickers for the portfolio.

    Returns:
        list[str]: List of tickers in the portfolio
    """

    url = f"{BASEAPI}/portfolio/tickers"
    params = {"id": portfolioId, "universe_size": universe_size}
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    response = response.json()
    return response["tickers"]
