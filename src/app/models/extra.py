# src/app/models/engagement.py
from tortoise import fields
from src.app.models.base import AbstractBaseModel, TimestampMixin


class Review(AbstractBaseModel, TimestampMixin):
    """
    Модель для хранения отзывов пользователей о фильмах.
    
    Назначение:
        - Пользователи могут оценивать фильмы (1-10)
        - Оставлять текстовые отзывы
        - Администратор может модерировать отзывы (is_approved)
    
    Связи:
        - Many-to-One с UserAccount (один пользователь → много отзывов)
        - Many-to-One с Movie (один фильм → много отзывов)
    
    Ограничения:
        - unique_together: пользователь может оставить только ОДИН отзыв на фильм
        - rating: от 1 до 10 (валидация)
    
    Применение в приложении:
        - Отображение отзывов на странице фильма
        - Расчёт среднего рейтинга фильма
        - Фильтрация фильмов по рейтингу
    """
    
    user = fields.ForeignKeyField(
        "models.UserAccount",
        related_name="reviews",  # user.reviews → все отзывы пользователя
        on_delete=fields.CASCADE,  # Удалить пользователя → удалить его отзывы
        description="Пользователь, оставивший отзыв"
    )
    
    movie = fields.ForeignKeyField(
        "models.Movie",
        related_name="reviews",  # movie.reviews → все отзывы о фильме
        on_delete=fields.CASCADE,  # Удалить фильм → удалить его отзывы
        description="Фильм, на который оставлен отзыв"
    )
    
    rating = fields.IntField(
        description="Оценка от 1 до 10"
    )
    
    comment = fields.TextField(
        null=True,  # Может быть пустым (только оценка без текста)
        description="Текст отзыва"
    )
    
    is_approved = fields.BooleanField(
        default=False,  # По умолчанию отзыв не опубликован (требует модерации)
        description="Одобрен ли отзыв администратором"
    )
    
    class Meta:
        table = "reviews"
        # Один пользователь может оставить только ОДИН отзыв на фильм
        unique_together = (("user", "movie"),)
        # Индексы для ускорения поиска
        indexes = ("rating", "is_approved", "create_at")


class WatchHistory(AbstractBaseModel, TimestampMixin):
    """
    Модель для отслеживания истории просмотров фильмов.
    
    Назначение:
        - Записывать, какие фильмы смотрел пользователь
        - Сохранять прогресс просмотра (для функции "Продолжить просмотр")
        - Отмечать, досмотрел ли пользователь фильм до конца
    
    Связи:
        - Many-to-One с UserAccount (один пользователь → много записей в истории)
        - Many-to-One с Movie (один фильм → много записей в истории)
    
    Применение в приложении:
        - Раздел "История просмотров" в профиле пользователя
        - Функция "Продолжить просмотр" (показываем прогресс)
        - Статистика для администратора (какие фильмы популярны)
        - Рекомендации фильмов на основе просмотренного
    """
    
    user = fields.ForeignKeyField(
        "models.UserAccount",
        related_name="watch_history",  # user.watch_history → вся история пользователя
        on_delete=fields.CASCADE,
        description="Пользователь, который смотрел фильм"
    )
    
    movie = fields.ForeignKeyField(
        "models.Movie",
        related_name="watch_history",  # movie.watch_history → кто смотрел этот фильм
        on_delete=fields.CASCADE,
        description="Просмотренный фильм"
    )
    
    watched_at = fields.DatetimeField(
        auto_now_add=True,  # Автоматически устанавливается при создании
        description="Дата и время просмотра"
    )
    
    progress = fields.IntField(
        default=0,  # В секундах (0 = начало, 7200 = 2 часа)
        description="Прогресс просмотра в секундах"
    )
    
    is_completed = fields.BooleanField(
        default=False,  # По умолчанию не досмотрен
        description="Просмотрен ли фильм до конца"
    )
    
    class Meta:
        table = "watch_history"
        # Одна запись на пару пользователь-фильм (обновляем прогресс)
        unique_together = (("user", "movie"),)
        # Индексы для быстрого поиска
        indexes = ("watched_at", "is_completed", "user")
        # Сортировка по умолчанию: сначала новые просмотры
        ordering = ["-watched_at"]


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