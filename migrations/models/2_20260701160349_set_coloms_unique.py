from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_users_email_133a6f" ON "users" ("email");
        CREATE UNIQUE INDEX "uid_users_usernam_266d85" ON "users" ("username");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_users_usernam_266d85";
        DROP INDEX IF EXISTS "uid_users_email_133a6f";"""
