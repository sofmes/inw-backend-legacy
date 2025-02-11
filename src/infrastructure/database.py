import asyncpg

from domain.user import User


class DataError(Exception):
    """データ関連のエラー"""


class AlreadyCreatedError(DataError):
    """既にデータが作られている場合のエラー"""


class DataManager:
    """データを管理するクラス"""

    async def setup(self, database_url: str) -> None:
        """データベースをセットアップします。"""
        self.db = await asyncpg.create_pool(database_url)
        self.user = UserDataManager(self.db)

        await self._setup_per_data_manager()

    async def _setup_per_data_manager(self) -> None:
        async with self.db.acquire() as conn, conn.cursor() as cursor:
            await self.user.setup(cursor)


class UserDataManager:
    """ユーザーデータを管理するクラス"""

    def __init__(self, db: asyncpg.Pool) -> None:
        self.db = db

    async def setup(self, conn: asyncpg.Connection) -> None:
        """ユーザーデータの管理ができる状態にします。"""
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS user_table (
                email VARCHAR(320) NOT NULL,
                name VARCHAR(256),
                bio VARCHAR(1000),
                PRIMARY KEY (email)
            );"""
        )

    async def _exists_user(self, email: str, conn: asyncpg.Connection) -> bool:
        row = await conn.fetchrow(
            "SELECT COUNT(*) FROM user_table WHERE email = $1 LIMIT 1;", email
        )

        return row is not None

    async def create_user(self, email: str) -> None:
        """ユーザーを作成します。"""
        async with self.db.acquire() as conn, conn.transaction():
            if await self._exists_user(email, conn):
                raise AlreadyCreatedError
            else:
                await conn.execute(
                    "INSERT INTO user_table VALUES ($1, NULL, NULL);", email
                )

    async def set_user(self, email: str, *, name: str, bio: str) -> None:
        """ユーザーの情報を設定します。"""
        async with self.db.acquire() as conn, conn.transaction():
            await conn.execute(
                "UPDATE user_table SET name = %s, bio = %s WHERE email = %s;",
                (name, bio, email),
            )

    async def get_user(self, email: str) -> User | None:
        """ユーザーの情報を取得します。

        Returns:
            ユーザーの名前とプロフィールのタプルが返却されます。
            もしもユーザーが見つからなかった場合は、``None``が返却されます。"""
        async with self.db.acquire() as conn, conn.transaction():
            row = await conn.fetchrow(
                "SELECT name, bio FROM user_table WHERE email = %s LIMIT = 1;",
                (email,),
            )

            if row:
                return User(email=email, name=row[0], bio=row[1])
