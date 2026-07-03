import random

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from src.app.core.jinja2 import templates
from src.app.models.user import UserAccount
from src.app.models.movie import Movie
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
    
    other_films = await Movie.all().prefetch_related('genres')
    other_films = random.sample(other_films, k=5)
    
    
    return templates.TemplateResponse(
        request=request,
        name="index.html", 
        context={"title": "Главная - Онлайн-кинотеатр", "other_films": other_films}
    )


@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Сервер работает!"}


@router.get("/about")
async def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html"
    )


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
    
    movies = await Movie.all().prefetch_related("genres").order_by("-rating")
    
    
    return templates.TemplateResponse(
        request=request,
        name="movies.html",
        context={"title": "Каталог фильмов - Онлайн-Кинотеатр", "movies": movies}
    )


@router.get("/movie/{movie_id}")
async def movie_detail_page(request: Request, movie_id: int):
    """ Страница деталей фильма. Рендерит HTML-шаблон. """
    movie = await Movie.get_or_none(id=movie_id).prefetch_related("genres")
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    other_films = await Movie.all().exclude(id=movie.id).prefetch_related('genres')
    other_films = random.sample(other_films, k=5)
    
    return templates.TemplateResponse(
        request=request,
        name="movie_detail.html",
        context={"title": f"{movie.title} - Онлайн-Кинотеатр", "movie": movie, "other_films": other_films}
    )


@router.get("/movie/watch/{movie_id}")
async def watch_movie_page(request: Request, movie_id: int, current_user=Depends(get_current_user)):
    """ Страница просмотра фильма. Рендерит HTML-шаблон. """
    movie = await Movie.get_or_none(id=movie_id)
    
    if movie is None:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    movie = await Movie.get(id=movie_id).prefetch_related("genres")
    
    # Проверка доступа к премиум-контенту
    if movie.is_premium_only and (not current_user or not current_user.is_premium):
        raise HTTPException(status_code=403, detail="Доступ запрещен. Требуется премиум-подписка.")
    
    return templates.TemplateResponse(
        request=request,
        name="watch.html",
        context={"title": f"Смотреть {movie.title} - Онлайн-Кинотеатр", "movie": movie}
    )