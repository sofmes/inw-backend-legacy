"""ログインしているユーザー、つまり自分に関するAPI"""

from typing import Annotated

from fastapi import APIRouter, Depends

from domain.user import User
from web.helper.dependencies import user

router = APIRouter(prefix="/me")


@router.get("/")
def get_me(user: Annotated[User, Depends(user)]) -> User:
    """ユーザーデータを取得する。"""
    return user
