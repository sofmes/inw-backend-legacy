import asyncpg

from domain.idea import Idea


class IdeaDataManager:
    def __init__(self, db: asyncpg.Pool) -> None:
        self.db = db

    async def setup(self, conn: asyncpg.Connection) -> None:
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS idea (
                id SERIAL NOT NULL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(2000)
            );"""
        )
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS relation (
                idea_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL
            );"""
        )

    async def add(self, idea: Idea) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute(
                "INSERT INTO idea (name, description) VALUES ($1, $2);",
                idea.name,
                idea.description,
            )

            # 連想付けを作成する。
            if not idea.tag_ids:
                return

            await conn.executemany(
                "INSERT INTO relation VALUES ($1, $2);",
                map(lambda tag_id: (idea.id, tag_id), idea.tag_ids),
            )

    async def remove(self, idea_id: str) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute("DELETE FROM idea WHERE id = $1 LIMIT 1;", idea_id)

            # 連想付けの削除を行う。
            await conn.execute("DELETE FROM relation WHERE idea_id = $1;", idea_id)
