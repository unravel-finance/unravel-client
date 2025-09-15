"""
Decorators for the Unravel client library.
"""
import functools
from collections.abc import Callable

import requests


def handle_api_errors(func: Callable) -> Callable:
    """
    Decorator to handle API errors and provide detailed error messages.

    This decorator wraps functions that make HTTP requests and automatically
    handles error responses by extracting error messages from the API response
    and raising more informative exceptions.

    Args:
        func: The function to decorate (should make HTTP requests)

    Returns:
        The decorated function with enhanced error handling

    Raises:
        requests.HTTPError: With detailed error message from API response
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as e:
            response = getattr(e, "response", None)
            if response is not None:
                try:
                    error_data = response.json()
                    error_message = (
                        error_data.get("error")
                        or error_data.get("message")
                        or error_data.get("detail")
                        or error_data.get("description")
                        or "Unknown error"
                    )
                    raise requests.HTTPError(
                        f"{response.status_code} {response.reason}: {error_message}",
                        response=response,
                    )
                except (ValueError, KeyError, AttributeError):
                    raise e
            else:
                raise e

    return wrapper
