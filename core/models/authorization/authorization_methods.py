"""Module that contains all functions connected with authentication"""


from datetime import datetime

from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from core.configs.config import SECRET_KEY, ALGORITHM, BANNED
from core.exceptions.exceptions import credentials_exception
from core.models.users.users_methods import get_user_by_id, unban_user
from core.schemas.token_models import TokenData
from core.store.db_model import UserTable


def get_current_user(session: Session, token: str) -> UserTable:
    """gets user using jwt token

    :param session: Session
        (database session)
    :param token: str
        (user's jwt token)
    :return: UserTable
    """
    token_data = get_token_data(token)
    user = get_user_by_id(user_id=token_data.id, session=session)
    if user is None:
        raise credentials_exception
    check_ban_data(user, session)
    return user


def get_token_data(token: str) -> TokenData:
    """gets data of jwt token

    :param token: str
        (user's jwt token)
    :return: TokenData
    :raises: credentials_exception
    """
    try:
        token_data = decode_jwt(token)
    except JWTError:
        raise credentials_exception
    return token_data


def decode_jwt(token: str):
    """decodes jwt token

    :param token: str
        (user's jwt token)
    :return: TokenData
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    uid: int = payload.get('id')
    if uid is None:
        raise credentials_exception
    token_data = TokenData(id=uid)
    return token_data


def is_user_banned(user: UserTable) -> bool:
    """checks if user banned

    :param user: UserTable
        (checking user)
    :return: bool
    """
    if user.state == BANNED:
        return True
    return False


def is_ban_date_expired(user: UserTable) -> bool:
    """checks if user's ban term expired

    :param user: UserTable
        (user with ban)
    :return: bool
    """
    current_date = datetime.now()
    if current_date >= user.ban_term:
        return True
    return False


def check_ban_data(user: UserTable, session: Session) -> None:
    """checks the state of ban

    :param user: UserTable
        (user, whose ban should be checked)
    :param session: Session
        (database session)
    :return: None
    """
    if is_user_banned(user):
        if is_ban_date_expired(user):
            unban_user(user, session)
            return
        raise HTTPException(status_code=403, detail=f"You are banned till {user.ban_term}")


