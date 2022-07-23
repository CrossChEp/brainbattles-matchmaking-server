import datetime
import json
import random

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.configs.config import redis, QUEUE
from core.middlewares.redis_sessions import get_redis_table
from core.schemas.user_models import UserQueueModel
from core.store.db_model import UserTable


def add_user_to_queue(user: UserTable, subject: str) -> None:
    get_redis_table(QUEUE)
    queue = json.loads(redis.get(QUEUE))
    user_queue_model = create_user_queue_model(user, subject)
    if user_queue_model.dict() in queue:
        raise HTTPException(status_code=403, detail='User already in queue')
    queue.append(user_queue_model.dict())
    redis.set(QUEUE, json.dumps(queue))
    redis.expire(QUEUE, datetime.timedelta(hours=5))


def create_user_queue_model(user: UserTable, subject: str) -> UserQueueModel:
    user_queue_model = UserQueueModel(
        id=user.id,
        rank=user.rank,
        subject=subject
    )
    return user_queue_model