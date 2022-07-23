from pydantic import BaseModel


class UserMatchmakingModel(BaseModel):
    id: int
    nickname: str
    rank: str

    class Config:
        orm_mode = True


class UserQueueModel(BaseModel):
    id: int
    rank: str
    subject: str

    class Config:
        orm_mode = True
