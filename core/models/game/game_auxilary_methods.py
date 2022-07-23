from core.configs.config import GAME, QUEUE
from core.middlewares.redis_sessions import get_redis_table, get_redis_game_table
from core.schemas.user_models import UserGameModel
from core.store.db_model import UserTable, TaskTable


def find_user_in_game_by_id(user_id: int):
    games = get_redis_game_table()
    return games[user_id]


def find_user_in_game_as_opponent(user_id: int):
    games = get_redis_game_table()
    for user_games in games:
        if games[user_games]['opponent_id'] == user_id:
            return games[user_games]
    return False


def create_user_game_model(user: UserTable, opponent: dict, task: TaskTable,
                           token: str):
    game_model = UserGameModel(
        user_id=user.id,
        opponent_id=opponent['id'],
        task_id=task.id,
        game_token=token
    )
    return game_model

