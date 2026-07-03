from tortoise import fields

from .base import AbstractBaseModel, TimestampMixin


class Genre(AbstractBaseModel, TimestampMixin):
    """Жанры фильмов (Комедия, Драма и т.д.)"""
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "genres"


class Movie(AbstractBaseModel, TimestampMixin):
    """Фильмы и сериалы"""
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    release_year = fields.IntField()
    rating = fields.IntField(null=True, default=1)
    duration = fields.IntField(null=True, default=0) # Длительность в минутах
    country = fields.CharField(max_length=100, null=True)
    
    director = fields.CharField(max_length=100, null=True)
    actors = fields.TextField(null=True)  # Список актеров через запятую
    
    poster_url = fields.CharField(max_length=500, null=True)
    video_url = fields.CharField(max_length=500)
    is_premium_only = fields.BooleanField(default=False)
    
    # Связь многие-ко-многим: у фильма много жанров, у жанра много фильмов
    genres = fields.ManyToManyField("models.Genre", related_name="movies", through="movie_genres")

    class Meta:
        table = "movies"

