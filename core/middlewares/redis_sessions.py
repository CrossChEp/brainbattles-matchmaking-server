"""Module that contains all functions that creates and gets redis tables"""


import json

from core.configs.config import redis, GAME


def get_redis_table(table_name: str):
    """ gets redis table using table name
    :param table_name: str
        name of table
    :return: list
    """
    try:
        r = json.loads(redis.get(table_name))
        if not r:
            r = []
        return r
    except TypeError:
        redis.set(table_name, json.dumps([]))
        r = json.loads(redis.get(table_name))
        return r


def get_redis_game_table():
    """creates and gets redis game table

    :return: Dict
    """
    try:
        r = json.loads(redis.get(GAME))
        if not r:
            r = {}
        return r
    except TypeError:
        redis.set(GAME, json.dumps({}))
        r = json.loads(redis.get(GAME))
        return r
