import asyncpg

from infrastructure.database.user import UserDataManager


class DataManager:
    """データを管理するクラス"""

    async def setup(self, database_url: str) -> None:
        """データベースをセットアップします。"""
        self.db = await asyncpg.create_pool(database_url)
        self.user = UserDataManager(self.db)

        await self._setup_per_data_manager()

    async def close(self) -> None:
        """データベースとの接続を終了します。"""
        await self.db.close()

    async def _setup_per_data_manager(self) -> None:
        async with self.db.acquire() as conn, conn.transaction():
            await self.user.setup(conn)
