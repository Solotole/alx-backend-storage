#!/usr/bin/python3
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
r = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """
    Decorator to cache the result of the `get_page` function and
    count the number of times a URL is accessed.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: A wrapper function that caches the result and
        tracks the access count.
    """
    @wraps(method)
    def wrapper(url: str):
        """
        Wrapper function that implements caching and access counting.

        Args:
            url (str): The URL to fetch the HTML content from.

        Returns:
            str: The HTML content of the URL, either from the cache
            or by making a new HTTP request.
        """
        r.incr(f"count:{url}")
        cached_content = r.get(f"cached:{url}")
        if cached_content:
            return cached_content.decode('utf-8')
        content = method(url)
        r.setex(f"cached:{url}", 10, content)
        return content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a specified URL.

    This function makes an HTTP GET request to the provided URL and
    returns the HTML content. If decorated with `cache_page`, it also
    caches the content in Redis and tracks the number of accesses.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
