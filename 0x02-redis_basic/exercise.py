#!/usr/bin/python3
""" defining a basic class for string saving into redis """
import redis
import uuid
from typing import Union


class Cache:
    """ basic class Cache """
    def __init__(self):
        """ initialization method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method to store data """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
