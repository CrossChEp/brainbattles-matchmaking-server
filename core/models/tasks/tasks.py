from sqlalchemy.orm import Session

from core.configs.config import OPEN
from core.middlewares.database_session import generate_session
from core.store.db_model import TaskTable


def get_tasks():
    session: Session = next(generate_session())
    return session.query(TaskTable).filter_by(state=OPEN).all()

