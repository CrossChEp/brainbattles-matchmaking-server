"""Module that contains session generator of database"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_protocol = 'postgresql://postgres:4122@localhost:5432/brainbattles'
engine = create_engine(database_protocol)
session = sessionmaker(bind=engine)


def generate_session():
    """generates database session

    :return: Session
    """
    sess = session()
    try:
        yield sess
    finally:
        sess.close()
