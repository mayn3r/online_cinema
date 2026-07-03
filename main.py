import uvicorn
import uuid

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.app.core.lifespan import lifespan
from src.app.routers import routers
from src.app.middlewares import middlewares

STATIC_DIR = "./src/static"
POSTERS_DIR = "./movies_data/posters"

app = FastAPI(
    title="Онлайн-кинотеатр",
    description="Учебный проект для практики (2 курс)",
    version="0.1.0",
    lifespan=lifespan,
    timezone="UTC"
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount(f"/{uuid.uuid4()}/posters", StaticFiles(directory=str(POSTERS_DIR)), name="posters")

for middleware in middlewares:
    app.add_middleware(middleware)
    
    
for router in routers:
    app.include_router(router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)