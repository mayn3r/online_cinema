# Используем легкий образ Python
FROM python:3.11-slim

# Копируем бинарник uv из официального образа (это самый быстрый способ)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
# (Если у тебя есть uv.lock, он тоже скопируется благодаря маске)
COPY pyproject.toml uv.lock* ./

# Устанавливаем зависимости проекта
# uv sync сам создаст виртуальное окружение и поставит всё из pyproject.toml
RUN uv sync

# Копируем исходный код приложения
COPY main.py ./
COPY src/ ./src/

# Открываем порт для FastAPI
EXPOSE 8000

# Команда запуска по умолчанию (переопределяется в docker-compose для dev-режима)
# CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uv", "run", "main.py"]