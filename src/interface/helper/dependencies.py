"""システム全体で使えるFastAPIの依存関係を実装する場所"""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

from domain.user import User
from infrastructure.database import DataManager
from interface.helper import auth


def data(app: FastAPI) -> DataManager:
    """データ管理の依存関係"""
    return app.state.data


async def user(
    authorization: Annotated[str | None, Header()] = None,
    data: DataManager = Depends(data),
) -> User:
    """資格情報を元に、ログインしているユーザーの情報を取得する依存関係"""
    if authorization is None:
        raise HTTPException(401, "資格情報を設定してください。")

    email = auth.verify(authorization.replace("Bearer ", "", 1))
    if email is None:
        raise HTTPException(401, "資格情報が不正です。")

    user = await data.user.get_user(email)
    if user is None:
        raise HTTPException(400, "ユーザーが見つかりませんでした。")

    return user
