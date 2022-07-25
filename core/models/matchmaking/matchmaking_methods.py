"""Module that contains all main functions connected with queue redis table"""


import datetime
import json

from fastapi import HTTPException

from core.configs.config import redis, QUEUE
from core.middlewares.redis_sessions import get_redis_table
from core.models.matchmaking.matchmaking_auxilary_methods import find_user_in_queue_by_id
from core.schemas.user_models import UserQueueModel
from core.store.db_model import UserTable


def add_user_to_queue(user: UserTable, subject: str) -> None:
    """adds user to queue redis table

    :param user: UserTable
        (user that should be added to queue table)
    :param subject: str
        (selected subject)
    :return: None
    """
    queue = get_redis_table(QUEUE)
    user_queue_model = create_user_queue_model(user, subject)
    if user_queue_model.dict() in queue:
        raise HTTPException(status_code=403, detail='User already in queue')
    queue.append(user_queue_model.dict())
    redis.set(QUEUE, json.dumps(queue))
    redis.expire(QUEUE, datetime.timedelta(hours=5))


def create_user_queue_model(user: UserTable, subject: str) -> UserQueueModel:
    """creates user's game model

    :param user: UserTable
        (user whose model should be created)
    :param subject: str
        (selected subject)
    :return: UserQueueModel
    """
    user_queue_model = UserQueueModel(
        id=user.id,
        rank=user.rank,
        subject=subject
    )
    return user_queue_model


def leave_the_queue(user: UserTable) -> None:
    """removes user from queue model

    :param user: UserTable
    :return: None
    """
    queue = get_redis_table(QUEUE)
    user_queue = find_user_in_queue_by_id(user.id)
    queue.remove(user_queue)
    redis.set(QUEUE, json.dumps(queue))
