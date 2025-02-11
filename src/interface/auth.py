from typing import Annotated

from fastapi import APIRouter, Cookie, HTTPException, Request
from fastapi.responses import RedirectResponse

from interface.helper import auth
from interface.helper.env import home_url
from interface.helper.google import fetch_email, use_flow

router = APIRouter(prefix="/auth")


@router.get("/")
def auth_index() -> RedirectResponse:
    authorization_url, state = use_flow()
    response = RedirectResponse(url=authorization_url)
    response.set_cookie("oauth_state", state)
    return response


@router.get("/callback")
def auth_callback(
    request: Request, state: Annotated[str | None, Cookie()] = None
) -> RedirectResponse:
    if state is None:
        raise HTTPException(
            400, detail="Google認証に失敗したか、不正なリクエストです。"
        )

    email = fetch_email(state, str(request.url))
    token = auth.create_access_token(email)

    response = RedirectResponse(url=home_url)
    response.set_cookie("session", token)

    return response
