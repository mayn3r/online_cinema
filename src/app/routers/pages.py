from fastapi import APIRouter, Request
from src.app.core.jinja2 import templates

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