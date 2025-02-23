from google.auth import external_account_authorized_user
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

from web.helper.env import (
    client_secrets_file,
    google_client_id,
    oauth_callback_url,
)

SCOPES = "openid https://www.googleapis.com/auth/userinfo.email"


def use_flow():
    """Googleのログインの認証を開始する。"""
    flow = Flow.from_client_secrets_file(client_secrets_file, scopes=SCOPES)
    flow.redirect_uri = oauth_callback_url

    return flow.authorization_url(access_type="offline", include_granted_scopes="true")


def fetch_email(state, url):
    """Googleで使われてるメールアドレスを取得する。"""
    flow = Flow.from_client_secrets_file(
        client_secrets_file, scopes=SCOPES, state=state
    )
    flow.redirect_uri = oauth_callback_url
    flow.fetch_token(authorization_response=url)

    assert not isinstance(
        flow.credentials, external_account_authorized_user.Credentials
    )
    info = id_token.verify_oauth2_token(
        flow.credentials.id_token, requests.Request(), google_client_id
    )

    return info.get("email")
