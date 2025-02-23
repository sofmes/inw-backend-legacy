"""環境変数を用意するためのモジュール"""

from os import getenv as _getenv


def getenv(key: str) -> str:
    temp = _getenv(key)
    if temp is None:
        raise Exception(f"環境変数`{key}`が設定されていません。")
    return temp


secret_key = getenv("SECRET_KEY")
database_url = getenv("DATABASE_URL")
client_secrets_file = getenv("GOOGLE_OAUTH_CLIENT_SECRETS_FILE")
google_client_id = getenv("GOOGLE_CLIENT_ID")
oauth_callback_url = getenv("OAUTH_CALLBACK_URL")
home_url = getenv("HOME_URL")
