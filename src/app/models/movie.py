from tortoise import fields

from .base import AbstractBaseModel, TimestampMixin


class Genre(AbstractBaseModel, TimestampMixin):
    """Жанры фильмов (Комедия, Драма и т.д.)"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)

    class Meta:
        table = "genres"


class Movie(AbstractBaseModel, TimestampMixin):
    """Фильмы и сериалы"""
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    release_year = fields.IntField()
    
    video_url = fields.CharField(max_length=500)
    is_premium_only = fields.BooleanField(default=False)
    
    # Связь многие-ко-многим: у фильма много жанров, у жанра много фильмов
    genres = fields.ManyToManyField("models.Genre", related_name="movies", through="movie_genres")

    class Meta:
        table = "movies"