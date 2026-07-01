from pydantic import BaseModel

from src.app.schemas.enums.role_enums import RoleEnum

class ChangeBalanceRequest(BaseModel):
    email: str
    amount: int
    

class InputUserEmail(BaseModel):
    email: str


class ChangeRoleRequest(BaseModel):
    email: str
    role: RoleEnum