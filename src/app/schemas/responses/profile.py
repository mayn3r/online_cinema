from pydantic import BaseModel

class GetUserProfile(BaseModel):
    id: int
    email: str
    name: str
    username: str
    create_at: str