import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.app.core.lifespan import lifespan
from src.app.routers import routers

STATIC_DIR = "./src/static"

app = FastAPI(
    title="Онлайн-кинотеатр",
    description="Учебный проект для практики (2 курс)",
    version="1.0.0",
    lifespan=lifespan,
    timezone="UTC"
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)