from tortoise import Tortoise
from .config import settings


async def _init_tortoise(
    db_url: str | None = None,
    *,
    generate_schemas: bool = True
) -> None:
    await Tortoise.init(
        db_url=(db_url or settings.DATABASE_URL),
        modules={
            "models": ["src.app.models"]
        },
        # _enable_global_fallback=True,
        timezone="UTC"
    )
    if generate_schemas:
        await Tortoise.generate_schemas()