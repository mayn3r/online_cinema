from fastapi import HTTPException

from src.app.models.user import UserAccount

async def get_user(**kwargs) -> UserAccount:
    user = await UserAccount.get_or_none(**kwargs)
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user