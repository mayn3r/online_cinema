from fastapi import APIRouter, Depends, HTTPException, Request

from src.app.utils.depends import require_admin
from src.app.utils.orm import get_user
from src.app.models.user import UserAccount
from src.app.schemas.requests.admin import ChangeBalanceRequest, InputUserEmail, ChangeRoleRequest
from src.app.schemas.responses.admin import ChangeBalanceResponse, ChangeRoleResponse
from src.app.schemas.responses.profile import GetUserProfile


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin routers"],
    dependencies=[Depends(require_admin)]
)

@router.get("/is_admin")
async def admin_info(
    request: Request
):
    return {"admin": True}


@router.get("/user_profie", response_model=GetUserProfile)
async def get_user_profile(data: InputUserEmail) -> GetUserProfile:
    """ Получть данные о профиле пользователя """
    
    user: UserAccount = await get_user(email=data.email)
    
    return GetUserProfile(
        id=user.id,
        email=user.email,
        role=user.role,
        name=user.name,
        balance=user.balance,
        username=user.username,
        create_at=user.create_at
    )
    
    

@router.post("/add_balance", response_model=ChangeBalanceResponse)
async def add_balance(data: ChangeBalanceRequest) -> ChangeBalanceResponse:
    """ Добавить монеты пользоватею """
    
    user: UserAccount = await get_user(email=data.email)
    
    if 0 < data.amount < 10**6:
        user.balance += data.amount
    else:
        raise HTTPException(
            status_code=416,
            detail="The entered value is outside the available range"
        )
    
    await UserAccount.save(user)
    return ChangeBalanceResponse(
        email=user.email,
        balance=user.balance
    )




@router.post("/remove_balance", response_model=ChangeBalanceResponse)
async def remove_balance(data: ChangeBalanceRequest) -> ChangeBalanceResponse:
    """ Убавить монеты пользоватею """
    
    user: UserAccount = await get_user(email=data.email)
    
    if (0 < data.amount < 10**6) and (user.balance-data.amount > 0):
        user.balance -= data.amount
    else:
        raise HTTPException(
            status_code=416,
            detail="The entered value is outside the available range"
        )
    
    await UserAccount.save(user)
    return ChangeBalanceResponse(
        email=user.email,
        balance=user.balance
    )
    

@router.post("/change_role", response_model=ChangeRoleResponse)
async def change_role(data: ChangeRoleRequest) -> ChangeRoleResponse:
    """ Изменение роли пользователя или администратора """
    
    if data.role.value not in ("user", "admin"):
        raise HTTPException(status_code=400, detail="Non-existent role")
    
    user: UserAccount = await get_user(email=data.email)
    user.role = data.role
    
    await UserAccount.save(user)
    
    return ChangeRoleResponse(
        email=user.email,
        role=user.role
    )