"""Module that contains all routers, belonging to matchmaking server"""


from fastapi import APIRouter

from core.controllers.user_controllers import add_to_queue_controller, \
    add_to_game_controller, leave_game_controller, leave_queue_controller

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_queue(token: str, subject: str) -> None:
    """POST ``/api/matchmaking?=<jwt_token>``

    Adds user to queue

    :param token: str
        (user's jwt token for authentication)
    :param subject: str
        (school subject)
    :return: None
    """
    add_to_queue_controller(token, subject)


@matchmaking_router.post('/api/game')
def add_to_game(token: str) -> str:
    """POST ``/api/game?=<jwt_token>``

    Adds user to game redis table

    :param token: str
        (user's jwt token for authentication)
    :return: str (game token)
    """
    return add_to_game_controller(token)


@matchmaking_router.delete('/api/game')
def leave_game(token: str) -> None:
    """DELETE ``/api/game?=<jwt_token>``

    Removes user from game table

    :param token: str
        (user's jwt token)
    :return: None
    """
    leave_game_controller(token)


@matchmaking_router.delete('/api/matchmaking')
def leave_queue(token: str) -> None:
    """ DELETE ``/api/matchmaking?=<jwt_token>``

    Removes user from queue table

    :param token: str
        (user's jwt token)
    :return: None
    """
    leave_queue_controller(token)
