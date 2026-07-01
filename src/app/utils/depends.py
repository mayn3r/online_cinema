from fastapi import Depends, HTTPException, Request

from .orm import get_user
from src.app.core.auth_cfg import security
from src.app.models.user import UserAccount
from src.app.schemas.enums.role_enums import RoleEnum


async def get_current_user(data = Depends(security.token_required())):
    email = data.sub
    return await get_user(email=email)


async def require_admin(current_user: UserAccount = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def require_not_auth(request: Request):
    """
    Проверяет, что пользователь НЕ авторизован.
    Смотрит наличие токена в cookies.
    """
    
    # Проверяем access_token в куках
    token = request.cookies.get("access_token")
    
    if token:
        raise HTTPException(
            status_code=403,
            detail="Вы уже авторизованы"
        )
