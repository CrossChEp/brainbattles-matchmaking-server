import random
from typing import List, Dict

from core.configs.config import QUEUE, ranks
from core.middlewares.redis_sessions import get_redis_table
from core.schemas.user_models import UserQueueModel
from core.store.db_model import UserTable, TaskTable


def find_user_in_queue_by_id(user_id: int):
    queue = get_redis_table(QUEUE)
    for user in queue:
        if user['id'] == user_id:
            return user
    return None


def find_user_subject(user_id: int):
    queue = get_redis_table(QUEUE)
    for user in queue:
        if user['id'] == user_id:
            return user['subject']
    return None


def find_opponents_by_subject(user: UserTable, subject: str):
    queue = get_redis_table(QUEUE)
    opponents = []
    for user_queue in queue:
        if user_queue['id'] == user.id:
            continue
        if user_queue['subject'] == subject:
            opponents.append(user_queue)
    return opponents


def get_available_ranks(available_rank: str):
    ranks_list = [rank for rank in ranks.values()]
    available_ranks = []
    for index, rank in enumerate(ranks_list):
        if rank == available_rank:
            available_ranks.append(rank)
            available_ranks.append(ranks_list[index - 1])
            available_ranks.append(ranks_list[index + 1])
    return available_ranks


def find_opponents_by_rank(opponents: List[UserTable], user: UserTable):
    final_opponents = []
    available_ranks = get_available_ranks(user.rank)

    for opponent in opponents:
        if opponent['id'] != user.id and opponent['rank'] in available_ranks:
            final_opponents.append(opponent)
    return final_opponents


def get_random_element(array: list):
    random_index = random.randint(0, len(array) - 1)
    return array[random_index]


def find_task_by_subject(tasks: List[TaskTable], subject: str):
    filtered_tasks = []
    for task in tasks:
        if task.subject == subject:
            filtered_tasks.append(task)
    return filtered_tasks


def find_task_by_rank(tasks: List[TaskTable], user):
    filtered_tasks = []
    available_ranks = get_available_ranks(user.rank)
    for task in tasks:
        if task.rank in available_ranks:
            filtered_tasks.append(task)
    return filtered_tasks

