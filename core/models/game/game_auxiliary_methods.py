"""Module that contains all auxiliary functions connected with game
redis table

"""
import datetime
import json
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs.config import redis, GAME
from core.middlewares.database_session import generate_session
from core.middlewares.redis_sessions import get_redis_game_table
from core.models.matchmaking.matchmaking_auxilary_methods import find_task_by_subject, \
    find_task_by_rank, get_random_element
from core.models.tasks.tasks import get_tasks
from core.models.users.users_methods import get_user_by_id
from core.schemas.user_models import UserGameModel
from core.store.db_model import UserTable, TaskTable


def find_user_game_token_by_id(user_id: int):
    """finds the data of game, stored by the input id

    :param user_id: int
        (id of user)
    :return: Dict[UserGameModel]
    """
    games = get_redis_game_table()
    for token in games.keys():
        if str(user_id) in games[token]:
            return token
    return None


def find_user_in_game_as_opponent(user_id: int):
    """finds the data of game, stored by the input opponent id

    :param user_id: int
        (id of opponent)
    :return: Dict[UserGameModel]
    """
    games = get_redis_game_table()
    for token in games:
        for user_game in games[token]:
            if games[token][user_game]['opponent_id'] == user_id:
                return token
    return None


def get_user_opponent(user_id: int) -> UserTable:
    """searches the user's opponent and returns

    :param user_id: int
        (id of user)
    :return: UserTable
    """
    games = get_redis_game_table()
    session: Session = next(generate_session())
    game_token = find_user_in_game_as_opponent(user_id)
    if game_token:
        all_user_ids_in_game = list(games[game_token].keys())
        opponent = get_user_by_id(all_user_ids_in_game[0], session)
        return opponent
    return None


def check_is_user_already_has_game(user: UserTable) -> str:
    """checks is user already has game as opponent, and if yes,
    adds user to this game and returns game token

    :param user: UserTable
        (user who searches the game)
    :return: str
    """
    games = get_redis_game_table()
    user_opponent = get_user_opponent(user.id)
    if user_opponent:
        token = find_user_game_token_by_id(user_opponent.id)
        task_id = games[token][str(user_opponent.id)]['task_id']
        user_game_model = create_user_game_model(user.id, user_opponent.id, task_id)
        return add_user_to_game_redis_table(user_game_model, token)


def create_user_game_model(user_id: int, opponent_id: int, task_id: int) -> UserGameModel:
    """creates the user game model

    :param user_id: int
        (id of user, whose game model should be)
    :param opponent_id: int
        (opponent id)
    :param task_id: int
        (id of task, that was chosen in matchmaking)
    :return: UserGameModel
    """
    game_model = UserGameModel(
        user_id=user_id,
        opponent_id=opponent_id,
        task_id=task_id
    )
    return game_model


def get_game_task(subject: str, user: UserTable) -> TaskTable:
    """filters all task by user rank and chosen subject, then
    chooses the random one end returns

    :param subject: str
        (school subject)
    :param user: UserTable
        (user that started matchmaking)
    :return: TaskTable
    """
    tasks = get_tasks()
    tasks = find_task_by_subject(tasks, subject)
    if not tasks:
        raise HTTPException(status_code=404, detail='No such subject')
    tasks = find_task_by_rank(tasks, user)
    if not tasks:
        raise HTTPException(status_code=404, detail='There is no task')
    task = get_random_element(tasks)
    return task


def create_game_token(user: UserTable) -> str:
    """creates token for game

    :param user: UserTable
        (user that started matchmaking)
    :return: str (game token)
    """
    is_user_in_game = find_user_game_token_by_id(user.id)
    if is_user_in_game:
        return is_user_in_game
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890' \
               '-=~`!@#$%^&*()_+:"|'
    token_size = random.randint(0, len(alphabet))
    token = ''
    alphabet_list = list(alphabet)
    for i in range(token_size):
        token += alphabet_list[random.randint(0, len(alphabet) - 1)]
    return token


def add_user_to_game_redis_table(user_game_model: UserGameModel, game_token: str) -> str:
    """adds user to redis game table

    :param user_game_model: UserGameModel
        (game model of user that started matchmaking)
    :param game_token: str
        (game token)
    :return: str (game token)
    """
    games = get_redis_game_table()
    if game_token not in games:
        games[game_token] = {}
    games[game_token][user_game_model.user_id] = user_game_model.dict()
    redis.set(GAME, json.dumps(games))
    redis.expire(GAME, datetime.timedelta(hours=3))
    return game_token
