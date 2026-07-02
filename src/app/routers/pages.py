from fastapi import APIRouter, Depends, Request
from src.app.core.jinja2 import templates
from src.app.utils.depends import get_current_user

router = APIRouter(
    tags=["Main routers"]
)

# 8. Базовый маршрут (главная страница)
@router.get("/", include_in_schema=False)
async def root(request: Request):
    """
    Главная страница. Рендерит HTML-шаблон.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"title": "Главная - Онлайн-кинотеатр"}
    )


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Сервер работает!"}


@router.get("/login")
async def login_page(request: Request):
    """ Страница входа. Рендерит HTML-шаблон. """
    return templates.TemplateResponse(
        request=request,
        name="login.html", 
        context={"title": "Вход - Онлайн-кинотеатр"}
    )


@router.get("/register")
async def register_page(request: Request):
    """ Страница регистрации. Рендерит HTML-шаблон. """
    return templates.TemplateResponse(
        request=request,
        name="register.html", 
        context={"title": "Регистрация - Онлайн-кинотеатр"}
    )


@router.get("/profile")
async def profile_page(request: Request, current_user=Depends(get_current_user)):
    """ Страница профиля пользователя. Рендерит HTML-шаблон. """
    return templates.TemplateResponse(
        request=request,
        name="profile.html", 
        context={"title": "Профиль - Онлайн-кинотеатр", "user": current_user}
    )