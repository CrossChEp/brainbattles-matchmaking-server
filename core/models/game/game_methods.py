import datetime
import json
import random

from fastapi import HTTPException

from core.configs.config import GAME, redis
from core.middlewares.redis_sessions import get_redis_table, get_redis_game_table
from core.models.game.game_auxilary_methods import create_user_game_model, find_user_in_game_by_id, \
    find_user_in_game_as_opponent
from core.models.matchmaking.matchmaking_auxilary_methods import find_user_in_queue_by_id, find_user_subject, \
    find_opponents_by_subject, find_opponents_by_rank, get_random_element, find_task_by_subject, find_task_by_rank
from core.models.tasks.tasks import get_tasks
from core.schemas.user_models import UserGameModel
from core.store.db_model import UserTable


def create_game_token(user: UserTable) -> str:
    is_user_in_game = find_user_in_game_as_opponent(user.id)
    if is_user_in_game:
        return is_user_in_game['game_token']
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890' \
               '-=~`!@#$%^&*()_+:"|'
    token_size = random.randint(0, len(alphabet))
    token = ''
    alphabet_list = [char for char in alphabet]
    for i in range(token_size):
        token += alphabet_list[random.randint(0, len(alphabet) - 1)]
    return token


def add_user_to_game(user: UserTable):
    subject = find_user_subject(user.id)
    if not find_user_in_queue_by_id(user.id):
        raise HTTPException(status_code=403, detail='User not in queue')
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
        tasks = get_tasks()
        tasks = find_task_by_subject(tasks, subject)
        if not tasks:
            raise HTTPException(status_code=404, detail='No such subject')
        tasks = find_task_by_rank(tasks, user)
        if not tasks:
            raise HTTPException(status_code=404, detail='There is no task')
        task = get_random_element(tasks)
        token = create_game_token(user)
        user_game_model = create_user_game_model(user, opponent, task, token)
        return add_user_to_game_redis_table(user_game_model, token)


def add_user_to_game_redis_table(user_game_model: UserGameModel, game_token: str):
    games = get_redis_game_table()
    games[user_game_model.user_id] = user_game_model.dict()
    redis.set(GAME, json.dumps(games))
    redis.expire(GAME, datetime.timedelta(hours=3))
    return game_token

