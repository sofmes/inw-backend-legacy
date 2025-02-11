"""FastAPIのライフスパンを管理するモジュール"""

from fastapi import FastAPI

from infrastructure.database import DataManager
from interface.helper.env import database_url


async def lifespan(app: FastAPI) -> None:
    """データベースへの接続など、システムが使える状態にする。"""
    app.state.data = DataManager()
    await app.state.data.setup(database_url)
