import nanoid 

from fastapi import APIRouter, HTTPException, Request, Response, Depends

from src.app.schemas.requests.auth import LoginRequest, RegisterRequest
from src.app.schemas.responses.auth import TokenResponse, AuthResponse, AccessTokenResponse
from src.app.core.auth_cfg import security
from src.app.models import UserAccount
from src.app.utils import hashing, depends

router = APIRouter(
    prefix="/api/auth",
    tags=["Authorization"]
)

@router.post("/register", 
    status_code=201,
    dependencies=[Depends(depends.require_not_auth)],
    response_model=AuthResponse
)
async def register(data: RegisterRequest, response: Response) -> AuthResponse:
    """ Регистрация пользователя """
    
    if any(
        (
            await UserAccount.get_or_none(email=data.email), 
            await UserAccount.get_or_none(username=data.username)
        )
        ):
        raise HTTPException(
            status_code=409,
            detail="Почта или username уже зарегистрированы"
        )
    
    if data.username is None:
        data.username = data.email.split("@")[0] + "_" + nanoid.generate(size=8)
        
    
    user: UserAccount = await UserAccount.create(
        email=data.email,
        password_hash=hashing.hash_password(data.password),
        name=data.name,
        username=data.username
    )
    
    uid = user.email
    user_data = {
        "email": user.email,
        "role": user.role.value
    }
    
    access_token = security.create_access_token(
        uid=uid,
        data=user_data
    )
    refresh_token = security.create_refresh_token(
        uid=uid,
        data=user_data
    )
    
    
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
            status_code=401,
            detail="Invalid password"
        )
    
    
    uid = user.email
    user_data = {
        "email": user.email,
        "role": user.role.value
    }
    
    access_token = security.create_access_token(
        uid=uid,
        data=user_data
    )
    refresh_token = security.create_refresh_token(
        uid=uid,
        data=user_data
    )
    
    security.set_access_cookies(access_token, response, max_age=3600)
    security.set_refresh_cookies(refresh_token, response, max_age=86400*7)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
    

@router.post("/logout")
async def logout(response: Response):
    security.unset_access_cookies(response)
    security.unset_refresh_cookies(response)
    
    return {"success": True}


@router.post("/refresh", 
    status_code=201,
    response_model=AccessTokenResponse
)
async def update_access_token(
        request: Request, 
        current_user = Depends(security.refresh_token_required)
) -> AccessTokenResponse:
    """ Обновление access токена """
    user = await UserAccount.get_or_none(email=current_user.sub)
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    user_data = {
        "email": user.email,
        "role": user.role.value
    }
    
    access_token = security.create_access_token(
        uid=user.email,
        data=user_data
    )
    
    return AccessTokenResponse(access_token=access_token)
    