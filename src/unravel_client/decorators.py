"""
Decorators for the Unravel client library.
"""
from collections.abc import Callable

import requests
import time


def retry_on_error(num_trials: int = 3, wait: float = 2.0):
    """
    Decorator to retry a function on exception.

    Args:
        num_trials (int): Number of attempts before giving up.
        wait (float): Seconds to wait between attempts.

    Returns:
        Decorated function that retries on error.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, num_trials + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    last_exception = e
                    if attempt == num_trials:
                        break
                    time.sleep(wait)
            if last_exception is not None:
                raise last_exception
            return None

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


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

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
