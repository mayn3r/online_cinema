from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise

from .db import _init_tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _init_tortoise(db_url="sqlite://data/sqlite.db", generate_schemas=True)
    
    yield
    
    await Tortoise.close_connections()
    