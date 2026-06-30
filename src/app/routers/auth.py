from fastapi import APIRouter, Depends, HTTPException, Request, Response

from src.app.schemas.requests.auth import LoginRequest, RegisterRequest
from src.app.schemas.responses.auth import TokenResponse, AuthResponse
from src.app.core.auth_cfg import security
from src.app.models import UserAccount
from src.app.utils import hashing

router = APIRouter(
    prefix="/api/auth",
    tags=["Authorization"]
)



@router.post("/register", status_code=201, response_model=AuthResponse)
async def register(data: RegisterRequest, request: Request, response: Response) -> AuthResponse:
    """ Регистрация пользователя """
    
    if request.cookies.get("access_token"):
        raise HTTPException(
            status_code=403,
            detail="Вы уже авторизованы"
        )
    
    if await UserAccount.get_or_none(email=data.email):
        raise HTTPException(
            status_code=409,
            detail="Почта уже зарегистрирована"
        )
        
    
    user: UserAccount = await UserAccount.create(
        email=data.email,
        password_hash=hashing.hash_password(data.password),
        name=data.name,
        username=data.username
    )
    
    uid = user.email
    user_data = {
        "email": user.email,
        "role": "user"
    }
    
    access_token = security.create_access_token(
        uid=uid,
        user_claims=user_data
    )
    refresh_token = security.create_refresh_token(
        uid=uid,
        user_claims=user_data
    )
    
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     # httponly=True,  # Недоступно для JS
    #     # secure=True,    # Только HTTPS
    #     samesite="lax", # Защита от CSRF
    #     max_age=3600    # 1 час
    # )
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=86400 * 7  # 7 дней
    # )
    
    security.set_access_cookies(access_token, response, max_age=3600)
    security.set_refresh_cookies(refresh_token, response, max_age=86400*7)
    
    return AuthResponse(
        type="register",
        id=user.id,
        email=user.email,
        name=user.name,
        username=user.username,
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )



@router.post("/login", status_code=201, response_model=TokenResponse)
async def login(data: LoginRequest, response: Response) -> TokenResponse:
    user = await UserAccount.get_or_none(email=data.email)
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    if not hashing.verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401
        )
    
    
    uid = user.email
    user_data = {
        "email": user.email,
        "role": "user"
    }
    
    
    access_token = security.create_access_token(
        uid=uid,
        user_claims=user_data
    )
    refresh_token = security.create_refresh_token(
        uid=uid,
        user_claims=user_data
    )
    
    # response.set_cookie(
    #     key="access_token",
    #     value=access_token,
    #     # httponly=True,  # Недоступно для JS
    #     # secure=True,    # Только HTTPS
    #     samesite="lax", # Защита от CSRF
    #     max_age=3600    # 1 час
    # )
    # response.set_cookie(
    #     key="refresh_token",
    #     value=refresh_token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax",
    #     max_age=86400 * 7  # 7 дней
    # )
    
    security.set_access_cookies(access_token, response, max_age=3600)
    security.set_refresh_cookies(refresh_token, response, max_age=86400*7)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
    

@router.post(
    path="/logout", 
    dependencies=[Depends(security.access_token_required)]
)
async def logout(response: Response):
    security.unset_access_cookies(response)
    security.unset_refresh_cookies(response)
    
    return {"success": True}