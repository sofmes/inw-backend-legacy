from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from infrastructure.database import DataManager
from web.helper import auth
from web.helper.dependencies import data
from web.helper.env import home_url
from web.helper.google import fetch_email, use_flow

router = APIRouter(prefix="/auth")
logger = getLogger(__name__)


@router.get("/")
def auth_index() -> RedirectResponse:
    authorization_url, state = use_flow()
    response = RedirectResponse(url=authorization_url)
    response.set_cookie("oauth_state", state)
    return response


@router.get("/callback")
async def auth_callback(
    request: Request,
    data: Annotated[DataManager, Depends(data)],
    oauth_state: Annotated[str | None, Cookie()] = None,
    error: str | None = None,
) -> RedirectResponse:
    if error is not None:
        logger.warning(
            "OAuth2人称に失敗したリクエストがあります。エラー内容：%s", error
        )
        return RedirectResponse("/auth")

    if oauth_state is None:
        raise HTTPException(
            400, detail="Google認証に失敗したか、不正なリクエストです。"
        )

    # Googleからメールアドレスを提供してもらう。
    email = fetch_email(oauth_state, str(request.url))

    # もしまだ登録したことないユーザーなら、データベースにユーザー情報を保存する。
    if await data.user.get_user(email) is None:
        await data.user.create_user(email)

    # 次ログインできるよう、ログインデータをクッキーに保存する。
    token = auth.create_access_token(email)

    response = RedirectResponse(url=home_url)
    response.set_cookie("session", token)

    return response
