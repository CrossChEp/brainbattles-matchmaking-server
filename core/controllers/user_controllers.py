from sqlalchemy.orm import Session

from core.middlewares.database_session import generate_session
from core.models.authorization.authorization_methods import get_current_user
from core.models.matchmaking_methods import add_user_to_queue


def add_to_queue_controller(token: str, subject: str) -> None:
    session: Session = next(generate_session())
    user = get_current_user(token=token, session=session)
    add_user_to_queue(user, subject)

