"""Module that contains all user controllers"""


from sqlalchemy.orm import Session

from core.middlewares.database_session import generate_session
from core.models.authorization.authorization_methods import get_current_user
from core.models.game.game_methods import add_user_to_game, leave_the_game
from core.models.matchmaking.matchmaking_methods import add_user_to_queue, leave_the_queue


def add_to_queue_controller(token: str, subject: str) -> None:
    """calls function that adds user to queue

    :param token: str
        (user's jwt token)
    :param subject: str
        (school subject)
    :return: None
    """
    session: Session = next(generate_session())
    user = get_current_user(token=token, session=session)
    add_user_to_queue(user, subject)


def add_to_game_controller(token: str) -> str:
    """calls function that adds user to game

    :param token: str
        (user's jwt token)
    :return: str (game token)
    """
    session: Session = next(generate_session())
    user = get_current_user(session, token)
    return add_user_to_game(user)


def leave_game_controller(token: str) -> None:
    """calls function that removes user from game

    :param token: str
        (user's jwt token)
    :return: None
    """
    session: Session = next(generate_session())
    user = get_current_user(token=token, session=session)
    leave_the_game(user)


def leave_queue_controller(token: str) -> None:
    """calls function that removes user from queue

    :param token: str
        (user's jwt token)
    :return: None
    """
    session: Session = next(generate_session())
    user = get_current_user(token=token, session=session)
    leave_the_queue(user)
