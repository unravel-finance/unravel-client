"""
Decorators for the Unravel client library.
"""

import time
from collections.abc import Callable

import requests


def transform_exception(exception: Exception) -> Exception:
    if not isinstance(exception, requests.HTTPError):
        return exception
    response = getattr(exception, "response", None)

    if response is None:
        return exception
    try:
        error_data = response.json()
        error_message = (
            error_data.get("error")
            or error_data.get("message")
            or error_data.get("detail")
            or error_data.get("description")
            or "Unknown error"
        )
        return requests.HTTPError(
            f"{response.status_code} {response.reason}: {error_message}",
            response=response,
        )
    except Exception:  # noqa: BLE001
        return exception


def retry_on_error(
    num_trials: int = 3,
    wait: float = 2.0,
    transform_exception: Callable = transform_exception,
):
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
                raise transform_exception(last_exception)
            return None

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator
