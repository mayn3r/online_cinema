from fastapi import APIRouter, Depends

from src.app.core.auth_cfg import security
from src.app.schemas.responses.profile import GetUserProfile
from src.app.models import UserAccount

router = APIRouter(
    prefix="/api/profile",
    tags=["User Profile API"]
)

@router.get("/info", response_model=GetUserProfile)
async def profile_info(current_user = Depends(security.token_required())) -> GetUserProfile:
    """ Получение информации о профиле """
    
    user = await UserAccount.get(email=current_user.sub)
    print(current_user)
    return GetUserProfile(
        id=user.id,
        email=user.email,
        role=current_user.role,
        name=user.name,
        balance=user.balance,
        username=user.username,
        create_at=user.create_at.strftime(r"%d.%m.%Y %X")
    )
    