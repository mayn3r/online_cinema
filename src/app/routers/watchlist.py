from fastapi import APIRouter, HTTPException, Depends

from src.app.core.auth_cfg import security
from src.app.utils import depends
from src.app.models import UserAccount, Movie, Watchlist
from src.app.schemas.requests.movie import GetMovieIdToWatchlist


router = APIRouter(
    prefix="/api/watchlist",
    tags=["Movies Watchlist API"],
    dependencies=[Depends(security.token_required())]
)


@router.post("/add")
async def add_movie_to_watchlist(
    mov: GetMovieIdToWatchlist,
    user: UserAccount = Depends(depends.get_current_user)
):
    """ Добавить фильм с избранное """
    
    movie_id = mov.movie_id
    
    movie = await Movie.get_or_none(id=movie_id)
    
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Фильм не найден"
        )
    
    # ID фильмов в избранных у пользователя
    ids = await user.watchlist.all().values_list("movie_id", flat=True)
    
    if movie_id in ids:
        raise HTTPException(
            status_code=409,
            detail="Фильм с таким ID уже сохранен в избранном"
        )
    
    await Watchlist.create(
        user=user,
        movie=movie
    )
    
    return {"status": "ok"}
    
    
    
@router.post("/remove")
async def remove_movie_to_watchlist(
    mov: GetMovieIdToWatchlist,
    user: UserAccount = Depends(depends.get_current_user)
):
    """ Удалить фильм с избранное """
    movie_id = mov.movie_id
    
    movie = await Movie.get_or_none(id=movie_id)
    
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Фильм не найден"
        )
    
    # ID фильмов в избранных у пользователя
    ids = await user.watchlist.all().values_list("movie_id", flat=True)
    
    if movie_id not in ids:
        raise HTTPException(
            status_code=409,
            detail="Фильм с таким ID не сохранен в избранном"
        )
    
    await Watchlist.filter(user=user, movie=movie).delete()
    
    return {"status": "ok"}
    
    