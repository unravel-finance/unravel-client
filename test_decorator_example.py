#!/usr/bin/env python3
"""
Example script to demonstrate the API error handling decorator.
This script shows how the decorator improves error messages for end users.
"""

import requests

from src.unravel_client.decorators import handle_api_errors


@handle_api_errors
def example_api_call_with_decorator(api_key: str):
    """Example function that makes an API call with the decorator."""
    url = "https://httpbin.org/status/401"  # Simulate 401 error
    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def example_api_call_without_decorator(api_key: str):
    """Example function that makes an API call without the decorator."""
    url = "https://httpbin.org/status/401"  # Simulate 401 error
    headers = {"X-API-KEY": api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("Testing API error handling decorator...")
    print("=" * 50)

    # Test without decorator (original behavior)
    print("1. Without decorator:")
    try:
        example_api_call_without_decorator("invalid_key")
    except requests.HTTPError as e:
        print(f"   Error: {e}")

    print()

    # Test with decorator (improved behavior)
    print("2. With decorator:")
    try:
        example_api_call_with_decorator("invalid_key")
    except requests.HTTPError as e:
        print(f"   Error: {e}")

    print()
    print("Note: The decorator will extract error messages from API responses")
    print("and provide more detailed error information to end users.")
