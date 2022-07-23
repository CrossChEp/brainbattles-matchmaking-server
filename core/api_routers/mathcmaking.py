from fastapi import APIRouter

from core.controllers.user_controllers import add_to_queue_controller

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_queue(token: str, subject: str):
    add_to_queue_controller(token, subject)

