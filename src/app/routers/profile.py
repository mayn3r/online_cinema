from fastapi import APIRouter, Depends

# from src.app.core.auth_cfg import security
from src.app.schemas.responses.profile import GetUserProfile
from src.app.models import UserAccount
from src.app.utils import depends

router = APIRouter(
    prefix="/api/profile",
    tags=["User Profile API"]
)

@router.get("/info", response_model=GetUserProfile)
async def profile_info(current_user: UserAccount = Depends(depends.get_current_user)) -> GetUserProfile:
    """ Получение информации о профиле """
    
    return GetUserProfile(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        name=current_user.name,
        balance=current_user.balance,
        username=current_user.username,
        create_at=current_user.create_at.strftime(r"%d.%m.%Y %X")
    )
    
