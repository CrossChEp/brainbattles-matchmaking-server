from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON, DATETIME, Date
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()


class UserTable(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    organization = Column(String)
    region = Column(String)
    contacts = Column(JSON)
    scores = Column(Float)
    rank = Column(String)
    wins = Column(Integer)
    games = Column(Integer)
    state = Column(String)
    ban_term = Column(Date)
    tasks = relationship('TaskTable', backref='user')


class TaskTable(base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subject = Column(String)
    content = Column(String)
    right_answer = Column(String)
    scores = Column(Float)
    rank = Column(String)
    author = Column(Integer, ForeignKey('users.id'))
    state = Column(String)

