"""Module that contains all auxiliary functions connected with game
redis table

"""


import random

from fastapi import HTTPException

from core.middlewares.redis_sessions import get_redis_game_table
from core.models.matchmaking.matchmaking_auxilary_methods import find_task_by_subject, \
    find_task_by_rank, get_random_element
from core.models.tasks.tasks import get_tasks
from core.schemas.user_models import UserGameModel
from core.store.db_model import UserTable, TaskTable


def find_user_in_game_by_id(user_id: int):
    """finds the data of game, stored by the input id

    :param user_id: int
        (id of user)
    :return: Dict[UserGameModel]
    """
    games = get_redis_game_table()
    return games[str(user_id)]


def find_user_in_game_as_opponent(user_id: int):
    """finds the data of game, stored by the input opponent id

    :param user_id: int
        (id of opponent)
    :return: Dict[UserGameModel]
    """
    games = get_redis_game_table()
    for user_games in games:
        if games[user_games]['opponent_id'] == user_id:
            return games[user_games]
    return None


def create_user_game_model(user: UserTable, opponent: dict, task: TaskTable,
                           token: str) -> UserGameModel:
    """creates the user game model

    :param user: UserTable
        (user, whose game model should be)
    :param opponent: Dict
        (opponent data of game)
    :param task: TaskTable
        (task, that was chosen in matchmaking)
    :param token: str
        (game token)
    :return: UserGameModel
    """
    game_model = UserGameModel(
        user_id=user.id,
        opponent_id=opponent['id'],
        task_id=task.id,
        game_token=token
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
    is_user_in_game = find_user_in_game_as_opponent(user.id)
    if is_user_in_game:
        return is_user_in_game['game_token']
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890' \
               '-=~`!@#$%^&*()_+:"|'
    token_size = random.randint(0, len(alphabet))
    token = ''
    alphabet_list = list(alphabet)
    for i in range(token_size):
        token += alphabet_list[random.randint(0, len(alphabet) - 1)]
    return token
