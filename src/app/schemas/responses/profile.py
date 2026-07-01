from pydantic import BaseModel

from src.app.schemas.enums import RoleEnum

class GetUserProfile(BaseModel):
    id: int
    email: str
    role: RoleEnum
    name: str
    balance: int
    username: str
    create_at: str