from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "reviews" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "create_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "rating" INT NOT NULL /* Оценка от 1 до 10 */,
    "comment" TEXT /* Текст отзыва */,
    "is_approved" INT NOT NULL DEFAULT 0 /* Одобрен ли отзыв администратором */,
    "movie_id" INT NOT NULL REFERENCES "movies" ("id") ON DELETE CASCADE /* Фильм, на который оставлен отзыв */,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE /* Пользователь, оставивший отзыв */,
    CONSTRAINT "uid_reviews_user_id_44b823" UNIQUE ("user_id", "movie_id")
) /* Модель для хранения отзывов пользователей о фильмах. */;
CREATE INDEX IF NOT EXISTS "idx_reviews_rating_d779bb" ON "reviews" ("rating", "is_approved", "create_at");
        CREATE TABLE IF NOT EXISTS "watch_history" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "create_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "watched_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* Дата и время просмотра */,
    "progress" INT NOT NULL DEFAULT 0 /* Прогресс просмотра в секундах */,
    "is_completed" INT NOT NULL DEFAULT 0 /* Просмотрен ли фильм до конца */,
    "movie_id" INT NOT NULL REFERENCES "movies" ("id") ON DELETE CASCADE /* Просмотренный фильм */,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE /* Пользователь, который смотрел фильм */,
    CONSTRAINT "uid_watch_histo_user_id_19ebbb" UNIQUE ("user_id", "movie_id")
) /* Модель для отслеживания истории просмотров фильмов. */;
CREATE INDEX IF NOT EXISTS "idx_watch_histo_watched_628686" ON "watch_history" ("watched_at", "is_completed", "user_id");
        CREATE TABLE IF NOT EXISTS "watchlist" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "create_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "added_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* Дата добавления в список */,
    "notes" TEXT /* Личные заметки пользователя (например, 'посмотреть с друзьями') */,
    "movie_id" INT NOT NULL REFERENCES "movies" ("id") ON DELETE CASCADE /* Фильм в списке желаемого */,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE /* Пользователь */,
    CONSTRAINT "uid_watchlist_user_id_1fc679" UNIQUE ("user_id", "movie_id")
) /* Модель для хранения списка фильмов, которые пользователь хочет посмотреть. */;
CREATE INDEX IF NOT EXISTS "idx_watchlist_added_a_2088e4" ON "watchlist" ("added_at", "user_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "watch_history";
        DROP TABLE IF EXISTS "watchlist";
        DROP TABLE IF EXISTS "reviews";"""
