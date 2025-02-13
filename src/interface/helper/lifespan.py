"""FastAPIのライフスパンを管理するモジュール"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.database import DataManager
from interface.helper.env import database_url


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    """データベースへの接続など、システムが使える状態にする。"""
    app.state.data = DataManager()
    await app.state.data.setup(database_url)
    yield
    await app.state.data.close()
