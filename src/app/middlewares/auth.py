from authx import TokenExpiredError
from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware
from src.app.core.jinja2 import templates
from src.app.core.auth_cfg import security
from src.app.models.user import UserAccount

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Получаем пользователя
        token = request.cookies.get("access_token")
        is_authenticated = False
        user = None
        
        token_expired = False
        
        if token:
            try:
                # Проверка токена
                decoded_token = security._decode_token(token)
                is_authenticated = True
                # user = {
                #     "email": decoded_token.sub, 
                #     "role": getattr(decoded_token, "role", None)
                # }
                user = await UserAccount.get(email=decoded_token.sub)
                
            except TokenExpiredError:
                token_expired = True
                
            except Exception:
                pass
        
        # Обновляем глобальные переменные Jinja2
        templates.env.globals.update({
            "is_authenticated": is_authenticated,
            "current_user": user
        })
        
        response = await call_next(request)
        
        if token_expired:
            response.delete_cookie("access_token")
        
        return response
