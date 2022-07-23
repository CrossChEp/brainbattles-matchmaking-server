from fastapi import APIRouter

from core.controllers.user_controllers import add_to_queue_controller, add_to_game_controller, leave_game_controller, \
    leave_queue_controller

matchmaking_router = APIRouter()


@matchmaking_router.post('/api/matchmaking')
def add_to_queue(token: str, subject: str):
    add_to_queue_controller(token, subject)


@matchmaking_router.post('/api/game')
def add_to_game(token: str):
    return add_to_game_controller(token)


@matchmaking_router.delete('/api/game')
def leave_game(token: str):
    leave_game_controller(token)


@matchmaking_router.delete('/api/matchmaking')
def leave_queue(token: str):
    leave_queue_controller(token)
