#!/usr/bin/python3
""" defining a basic class for string saving into redis """
from redis import Redis
import uuid
from typing import Union, Callable, Optional

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
        self._redis: Redis = Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in the Redis cache.

        This method generates a random key using uuid,
        stores the data in Redis using
        this key, and returns the key.
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
