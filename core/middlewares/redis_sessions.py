import json

from core.configs.config import redis, GAME


def get_redis_table(table_name: str):
    """ gets redis table using table name
    :param table_name: str
        name of table
    """
    try:
        r = json.loads(redis.get(table_name))
        if not r:
            r = []
        return r
    except TypeError:
        redis.set(table_name, json.dumps([]))


def get_redis_game_table():
    try:
        r = json.loads(redis.get(GAME))
        if not r:
            r = {}
        return r
    except TypeError:
        redis.set(GAME, json.dumps({}))

