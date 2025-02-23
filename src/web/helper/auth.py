"""ログインに使う資格情報に関するモジュール"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from web.helper.env import secret_key

ALGORITHM = "HS256"


def create_access_token(sub: str, expires_delta: timedelta | None = None) -> str:
    """トークンの作成を行う。"""
    to_encode: dict[str, Any] = {"sub": sub}

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)

    return encoded_jwt


def verify(token: str) -> str | None:
    """認証をしてユーザーのメールアドレスを取り出す。"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return
