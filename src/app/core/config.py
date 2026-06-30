from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    
    JWT_SECRET_KEY: SecretStr = SecretStr("*")

    # Указываем, откуда брать переменные
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# TORTOISE_ORM для Aerich
TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://data/sqlite.db",#settings.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "src.app.models",    # Ваши модели
                "aerich.models"      # Модели Aerich (обязательно!)
            ],
            "default_connection": "default",
        }
    },
    "timezone": "UTC",
}