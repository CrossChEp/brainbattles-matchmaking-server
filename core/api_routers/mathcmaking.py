from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.schemas import UserMatchmakingModel

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_queue(user_token: str, user: UserMatchmakingModel):
    pass
