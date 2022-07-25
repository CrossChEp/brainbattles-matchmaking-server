"""Module that contains all custom exceptions"""


from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

credentials_exception = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


user_not_in_queue_exception = HTTPException(
    status_code=403,
    detail="User not in queue"
)


user_not_in_game_exception = HTTPException(
    status_code=403,
    detail="User not in game"
)

user_already_in_queue_exception = HTTPException(
    status_code=403,
    detail="User already in queue"
)


user_already_in_game_exception = HTTPException(
    status_code=403,
    detail="User already in game"
)
