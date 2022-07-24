"""Module that contains all auxiliary functions connected with queue
redis table

"""


import random
from typing import List, Dict

from core.configs.config import QUEUE, ranks
from core.middlewares.redis_sessions import get_redis_table
from core.schemas.user_models import UserQueueModel
from core.store.db_model import UserTable, TaskTable


def find_user_in_queue_by_id(user_id: int):
    """ finds user in queue using his id

    :param user_id: int
        (id of user)
    :return: dict
    """
    queue = get_redis_table(QUEUE)
    for user in queue:
        if user['id'] == user_id:
            return user
    return None


def find_user_subject(user_id: int) -> str:
    """finds subject that user chose in start of matchmaking

    :param user_id: int
        (id of user)
    :return: str
    """
    queue = get_redis_table(QUEUE)
    for user in queue:
        if user['id'] == user_id:
            return user['subject']
    return None


def find_opponents_by_subject(user: UserTable, subject: str):
    """finds opponents by user's chosen subject

    :param user: UserTable
        (user that started matchmaking)
    :param subject: str
        (chosen subject)
    :return: dict
    """
    queue = get_redis_table(QUEUE)
    opponents = []
    for user_queue in queue:
        if user_queue['id'] == user.id:
            continue
        if user_queue['subject'] == subject:
            opponents.append(user_queue)
    return opponents


def get_available_ranks(available_rank: str) -> List[str]:
    """gets all ranks regarding user's rank

    :param available_rank: str
        (user rank)
    :return: List[str]
    """
    ranks_list = [rank for rank in ranks.values()]
    available_ranks = []
    for index, rank in enumerate(ranks_list):
        if rank == available_rank:
            available_ranks.append(rank)
            available_ranks.append(ranks_list[index - 1])
            available_ranks.append(ranks_list[index + 1])
    return available_ranks


def find_opponents_by_rank(opponents: List[UserTable], user: UserTable) -> List[UserTable]:
    """finds all opponents regarding user's rank

    :param opponents: List[UserTable]
        (filtered users by subject)
    :param user: UserTable
        (user that started matchmaking)
    :return: List[UserTable]
    """
    final_opponents = []
    available_ranks = get_available_ranks(user.rank)

    for opponent in opponents:
        if opponent['id'] != user.id and opponent['rank'] in available_ranks:
            final_opponents.append(opponent)
    return final_opponents


def get_random_element(array: list):
    """gets random element in list

    :param array: List[Any]
        (list where random element should be found)
    :return: Any
    """
    random_index = random.randint(0, len(array) - 1)
    return array[random_index]


def find_task_by_subject(tasks: List[TaskTable], subject: str) -> List[TaskTable]:
    """filters task by selected subject

    :param tasks: List[TaskTable]
        (tasks)
    :param subject: str
        (selected subject)
    :return:
    """
    filtered_tasks = []
    for task in tasks:
        if task.subject == subject:
            filtered_tasks.append(task)
    return filtered_tasks


def find_task_by_rank(tasks: List[TaskTable], user: UserTable) -> List[TaskTable]:
    """filters tasks by user's rank

    :param tasks: List[TaskTable]
        (tasks)
    :param user: UserTable
        (user that started matchmaking)
    :return: List[TaskTable]
    """
    filtered_tasks = []
    available_ranks = get_available_ranks(user.rank)
    for task in tasks:
        if task.rank in available_ranks:
            filtered_tasks.append(task)
    return filtered_tasks

