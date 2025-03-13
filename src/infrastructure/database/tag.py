import asyncpg

from domain.tag import Tag


class TagDataManager:
    def __init__(self, db: asyncpg.Pool) -> None:
        self.db = db

    async def setup(self, conn: asyncpg.Connection) -> None:
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS tag (
                id SERIAL NOT NULL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );"""
        )

    async def add(self, tag: Tag) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute("INSERT INTO tag VALUES ($1, $2);", tag.id, tag.name)

    async def remove(self, tag_id: int) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute("DELETE FROM tag WHERE id = $1", tag_id)
