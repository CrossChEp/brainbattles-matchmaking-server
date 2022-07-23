from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """ Scheme of token

        fields:
        access_token: str
            jwt token
        token_type: str
            type of token
    """
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    """ Scheme of token with user's username
        fields:
        username: Optional[str]
    """
    id: Optional[int] = None

    class Config:
        orm_mode = True
