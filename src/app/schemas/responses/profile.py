from pydantic import BaseModel

class GetUserProfile(BaseModel):
    id: int
    email: str
    name: str
    balance: int
    username: str
    create_at: str