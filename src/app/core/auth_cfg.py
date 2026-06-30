from authx import AuthXConfig, AuthX

from .config import settings


config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY.get_secret_value(),
    JWT_TOKEN_LOCATION = ["cookies"],
    JWT_ACCESS_COOKIE_NAME = "access_token",
    JWT_REFRESH_COOKIE_NAME = "refresh_token",
    JWT_COOKIE_CSRF_PROTECT = False,
    JWT_COOKIE_HTTP_ONLY=False,
    JWT_COOKIE_SECURE=False,
    JWT_COOKIE_SAMESITE = "lax"
    
)

security = AuthX(config=config)