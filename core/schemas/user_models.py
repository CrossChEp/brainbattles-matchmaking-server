from pydantic import BaseModel


class UserMatchmakingModel(BaseModel):
    id: int
    nickname: str
    rank: str

    class Config:
        orm_mode = True
