from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "movies" ADD "duration" INT DEFAULT 0;
        ALTER TABLE "movies" ADD "director" VARCHAR(100);
        ALTER TABLE "movies" ADD "actors" TEXT;
        ALTER TABLE "movies" ADD "country" VARCHAR(100);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "movies" DROP COLUMN "duration";
        ALTER TABLE "movies" DROP COLUMN "director";
        ALTER TABLE "movies" DROP COLUMN "actors";
        ALTER TABLE "movies" DROP COLUMN "country";"""
