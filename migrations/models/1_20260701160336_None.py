from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "genres" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "create_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(50) NOT NULL UNIQUE
) /* Жанры фильмов (Комедия, Драма и т.д.) */;
CREATE TABLE IF NOT EXISTS "movies" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "create_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "release_year" INT NOT NULL,
    "video_url" VARCHAR(500) NOT NULL,
    "is_premium_only" INT NOT NULL DEFAULT 0
) /* Фильмы и сериалы */;
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "create_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "email" VARCHAR(64) NOT NULL,
    "password_hash" VARCHAR(512) NOT NULL,
    "name" VARCHAR(128) NOT NULL,
    "balance" INT NOT NULL DEFAULT 0,
    "username" VARCHAR(32) NOT NULL,
    "is_premium" INT NOT NULL DEFAULT 0,
    "role" VARCHAR(5) NOT NULL DEFAULT 'user' /* USER: user\nADMIN: admin */
) /* Модель пользователя  */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "movie_genres" (
    "movies_id" INT NOT NULL REFERENCES "movies" ("id") ON DELETE CASCADE,
    "genre_id" INT NOT NULL REFERENCES "genres" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_movie_genre_movies__a26614" ON "movie_genres" ("movies_id", "genre_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
