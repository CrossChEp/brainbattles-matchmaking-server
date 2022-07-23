import datetime
import json

from fastapi import HTTPException

from core.configs.config import GAME, redis
from core.middlewares.redis_sessions import get_redis_game_table
from core.models.game.game_auxilary_methods import create_user_game_model, get_game_task, create_game_token
from core.models.matchmaking.matchmaking_auxilary_methods import find_user_in_queue_by_id, find_user_subject, \
    find_opponents_by_subject, find_opponents_by_rank, get_random_element
from core.schemas.user_models import UserGameModel
from core.store.db_model import UserTable


def add_user_to_game(user: UserTable):
    if not find_user_in_queue_by_id(user.id):
        raise HTTPException(status_code=403, detail='User not in queue')
    subject = find_user_subject(user.id)
    return user_game_adding(user, subject)


def user_game_adding(user: UserTable, subject: str):
    while True:
        opponents = find_opponents_by_subject(user, subject)
        if not opponents:
            continue
        opponents = find_opponents_by_rank(opponents, user)
        if not opponents:
            continue
        opponent = get_random_element(opponents)
        task = get_game_task(subject, user)
        token = create_game_token(user)
        user_game_model = create_user_game_model(user, opponent, task, token)
        return add_user_to_game_redis_table(user_game_model, token)


def add_user_to_game_redis_table(user_game_model: UserGameModel, game_token: str):
    games = get_redis_game_table()
    games[user_game_model.user_id] = user_game_model.dict()
    redis.set(GAME, json.dumps(games))
    redis.expire(GAME, datetime.timedelta(hours=3))
    return game_token

