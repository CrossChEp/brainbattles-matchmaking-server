from datetime import datetime

from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from core.configs.config import SECRET_KEY, ALGORITHM, BANNED
from core.models.users.users_methods import get_user_by_id, unban_user
from core.schemas.token_models import TokenData
from core.store.db_model import UserTable


def get_current_user(session: Session, token: str):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: int = payload.get('id')
        if uid is None:
            raise credentials_exception
        token_data = TokenData(id=uid)
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(user_id=token_data.id, session=session)
    if user is None:
        raise credentials_exception
    check_ban_data(user, session)
    return user


def is_user_banned(user: UserTable) -> bool:
    if user.state == BANNED:
        return True
    return False


def is_ban_date_expired(user: UserTable) -> bool:
    current_date = datetime.now()
    if current_date >= user.ban_term:
        return True
    return False


def check_ban_data(user: UserTable, session: Session) -> None:
    if is_user_banned(user):
        if is_ban_date_expired(user):
            unban_user(user, session)
            return
        raise HTTPException(status_code=403, detail=f"You are banned till {user.ban_term}")


