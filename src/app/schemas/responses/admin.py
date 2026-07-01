from pydantic import BaseModel

from src.app.schemas.enums.role_enums import RoleEnum

class ChangeBalanceResponse(BaseModel):
    email: str
    balance: int


class ChangeRoleResponse(BaseModel):
    email: str
    role: RoleEnum