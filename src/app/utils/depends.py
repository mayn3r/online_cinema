from fastapi import Depends, HTTPException

from .orm import get_user
from src.app.core.auth_cfg import security
from src.app.models.user import UserAccount


def require_admin(get_current_user = Depends(security.token_required())):
    role = get_current_user.role
    
    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )
    
    return get_current_user


def require_not_auth(get_current_user = Depends(security.token_required())):
    if get_current_user:
        raise HTTPException(
            status_code=403,
            detail="Вы уже авторизованы"
        )
    
    return get_current_user


async def get_current_user(data = Depends(security.token_required())):
    email = data.sub
    
    user: UserAccount = await get_user(email=email)
    
    return user