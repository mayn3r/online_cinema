from pydantic import BaseModel


class GetMovieIdToWatchlist(BaseModel):
    movie_id: int