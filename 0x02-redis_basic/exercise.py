#!/usr/bin/env python3
""" defining a basic class for string saving into redis """
import redis
import uuid
from functools import wraps
import requests
from typing import Union, Callable, Optional, Any, List


class Cache:
    """
    A Cache class that interacts with a Redis
    database to store and retrieve data.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache class.

        This method creates a Redis client instance
        and flushes the database to ensure
        it starts empty.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of calls to a method
        and store the count in Redis.
        Args:
            method (Callable): The method to be decorated.
        Returns:
            Callable: A wrapper function that increments the call
            count and then calls the original method.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            method_name = method.__qualname__
            self._redis.incr(method_name)
            result = method(self, *args, **kwargs)
            return result
        return wrapper

    def call_history(method: Callable) -> Callable:
        """
        Decorator to store the history of inputs and outputs
        for a particular function.
        Args:
            method (Callable): The method to be decorated.
        Returns:
            Callable: A wrapper function that logs the input arguments
                      and output of the decorated method.
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            method_name = method.__qualname__
            input_key = f"{method_name}:inputs"
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            output_key = f"{method_name}:outputs"
            self._redis.rpush(output_key, str(output))

            return output
        return wrapper

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis cache.

        This method generates a random key using uuid,
        stores the data in Redis using
        this key, and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes], Any]] = None) -> Any:
        """
        Retrieves data from Redis for the given key and optionally
        applies a conversion function.
        Args:
            key (str): The key to retrieve data for.
            fn (Optional[Callable[[bytes], Any]], optional): A function
            to convert the retrieved data (default: None).
        Returns:
            The retrieved data converted using the provided function,
            or None if the key doesn't exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        else:
            return value

    def get_str(self, key: str) -> str:
        """
        Retrieves data from Redis for the given key,
        assuming it's stored as a UTF-8 string.
        Args:
            key (str): The key to retrieve data for.
        Returns:
            The retrieved data decoded as a UTF-8 string,
            or None if the key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieves data from Redis for the given key,
        assuming it's stored as an integer.
        Args:
            key (str): The key to retrieve data for.
        Returns:
            The retrieved data converted to an integer,
            or None if the key doesn't exist.
        """
        return self.get(key, fn=int)

    def replay(method: Callable) -> None:
        """
        Display the history of calls of a particular function.
        Args:
            method (Callable): The method to replay history for.
        """
        method_name = method.__qualname__
        ref = method.__self__._redis
        inputs: List[bytes] = ref.lrange(f"{method_name}:inputs", 0, -1)
        outputs: List[bytes] = ref.lrange(f"{method_name}:outputs", 0, -1)
        print(f"{method_name} was called {len(inputs)} times:")
        for input_, output in zip(inputs, outputs):
            input_str = input_.decode("utf-8")
            output_str = output.decode("utf-8")
            print(f"{method_name}(*{input_str}) -> {output_str}")
