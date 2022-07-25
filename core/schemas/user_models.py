"""Module that contains all models connected with user

    classes:
        UserQueueModel
        UserGameModel
"""


from pydantic import BaseModel


class UserQueueModel(BaseModel):
    """scheme of user's queue redis cell

        fields:
            id: int
                id of user
            rank: str
                (rank of user)
            subject:
                (selected subject)
    """
    id: int
    rank: str
    subject: str

    class Config:
        orm_mode = True


class UserGameModel(BaseModel):
    """ scheme of user game redis cell

        fields:
            user_id: int
                (id of user)
            opponent_id: int
                (id of opponent)
            task_id: int
                (id of task)
            game_token: str
                (token of game)
    """
    user_id: int
    opponent_id: int
    task_id: int
    game_token: str

    class Config:
        orm_mode = True
