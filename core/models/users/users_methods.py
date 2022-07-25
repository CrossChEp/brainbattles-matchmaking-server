"""Module that contains all functions connected wth users"""


from sqlalchemy.orm import Session

from core.configs.config import DEFAULT
from core.store.db_model import UserTable


def get_user_by_id(user_id: int, session: Session) -> UserTable:
    """ gets user by user id

    :param user_id: int
        (user id)
    :param session: Session
    :return: User
    """

    user = session.query(UserTable).filter_by(id=user_id).first()
    return user


def unban_user(user: UserTable, session: Session) -> None:
    """removes user from ban state

    :param user: UserTable
        (user whose ban should be removed)
    :param session: Session
        (database session)
    :return: None
    """
    user.state = DEFAULT
    user.ban_term = None
    session.commit()
