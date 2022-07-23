from fastapi import APIRouter

from core.controllers.user_controllers import add_to_queue_controller, add_to_game_controller
from core.models.game.game_methods import add_user_to_game_redis_table

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_queue(token: str, subject: str):
    add_to_queue_controller(token, subject)


@matchmaking_router.post('/api/game')
def add_to_game(token: str):
    return add_to_game_controller(token)
