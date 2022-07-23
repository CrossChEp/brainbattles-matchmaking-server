from redis.client import Redis


SECRET_KEY = '.AvbsFG1Ro5hx,k2DMdSg307z!uTJ9NqViOjEWny?lUaCtrYIX4-KLHw_Bc6mfpe8QZP'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ranks = {
    0: 'rank 10',
    20: 'rank 9',
    76: 'rank 8',
    229: 'rank 7',
    643: 'rank 6',
    1768: 'rank 5',
    4829: 'rank 4',
    13147: 'rank 3',
    15200: 'rank 2',
    19621: 'rank 1',
    25000: 'pro rank 1',
    30000: 'pro rank 2',
    35890: 'pro rank 3',
    41781: 'pro rank 4',
}

redis = Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)

QUEUE = 'queue'
GAME = 'game'
DEFAULT = 'default'
HELPER = 'helper'
MODERATOR = 'moderator'
ADMIN = 'admin'
ELDER_ADMIN = 'elder_admin'
CEO = 'ceo'
BANNED = 'banned'
NOT_MODERATED = 'not_moderated'
OPEN = 'open'
HIDDEN = 'hidden'
