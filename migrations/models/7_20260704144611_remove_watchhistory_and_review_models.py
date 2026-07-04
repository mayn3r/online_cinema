from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "watch_history";
        DROP TABLE IF EXISTS "reviews";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
