from typing import Literal
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class AuthResponse(BaseModel):
    type: Literal["login", "register"]
    id: int
    email: str
    name: str
    username: str
    tokens: TokenResponse


class AccessTokenResponse(BaseModel):
    access_token: str