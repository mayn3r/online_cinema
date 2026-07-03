from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from src.app.core.jinja2 import templates
from src.app.models.user import UserAccount
from src.app.models.movie import Movie, Genre
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

@router.get("/@{username}")
async def user_profile_page(request: Request, username: str):
    user = await UserAccount.get_or_none(username=username)
    
    if user is None:
        # raise HTTPException(status_code=404, detail="Пользователь не найден")
        return RedirectResponse(url="/", status_code=302)
    
    """ Страница профиля пользователя. Рендерит HTML-шаблон. """
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={"title": f"Профиль пользователя {username} - Онлайн-кинотеатр", "user": user}
    )
    
    
@router.get("/movies")
async def movies_page(request: Request):
    """ Страница каталога фильмов. Рендерит HTML-шаблон. """
    import pprint
    
    # movies = await Movie.all().prefetch_related("genres").values(
    #     "id", "title", "description", "release_year", "video_url", "is_premium_only", "poster_url", "genres__name"
    # )
    
    movies = await Movie.all().prefetch_related("genres").order_by("-rating")
    
    pprint.pprint(movies[0].is_premium_only)
    
    return templates.TemplateResponse(
        request=request,
        name="movies.html",
        context={"title": "Каталог фильмов - Онлайн-Кинотеатр", "movies": movies}
    )