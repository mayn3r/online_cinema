# src/app/models/engagement.py
from tortoise import fields
from src.app.models.base import AbstractBaseModel, TimestampMixin


class Watchlist(AbstractBaseModel, TimestampMixin):
    """
    Модель для хранения списка фильмов, которые пользователь хочет посмотреть.
    
    Назначение:
        - Пользователь добавляет фильмы в "Избранное" / "Хочу посмотреть"
        - Удобный список для планирования просмотров
    
    Связи:
        - Many-to-One с UserAccount (один пользователь → много фильмов в списке)
        - Many-to-One с Movie (один фильм → может быть в списках многих пользователей)
    
    Применение в приложении:
        - Раздел "Мой список" / "Избранное" в профиле
        - Кнопка "Добавить в избранное" на странице фильма
        - Напоминания о непросмотренных фильмах
    
    Отличие от WatchHistory:
        - Watchlist = фильмы, которые ХОЧУ посмотреть (будущее)
        - WatchHistory = фильмы, которые УЖЕ посмотрел (прошлое)
    """
    
    user = fields.ForeignKeyField(
        "models.UserAccount",
        related_name="watchlist",  # user.watchlist → список желаемого пользователя
        on_delete=fields.CASCADE,
        description="Пользователь"
    )
    
    movie = fields.ForeignKeyField(
        "models.Movie",
        related_name="in_watchlists",  # movie.in_watchlists → в чьих списках этот фильм
        on_delete=fields.CASCADE,
        description="Фильм в списке желаемого"
    )
    
    added_at = fields.DatetimeField(
        auto_now_add=True,
        description="Дата добавления в список"
    )
    
    notes = fields.TextField(
        null=True,  # Может быть пустым
        description="Личные заметки пользователя (например, 'посмотреть с друзьями')"
    )
    
    class Meta:
        table = "watchlist"
        # Один фильм может быть в списке пользователя только ОДИН раз
        unique_together = (("user", "movie"),)
        # Индексы для быстрого поиска
        indexes = ("added_at", "user")
        # Сортировка по умолчанию: сначала недавно добавленные
        ordering = ["-added_at"]