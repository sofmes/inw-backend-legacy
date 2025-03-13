from pydantic import BaseModel, Field


class User(BaseModel):
    """ユーザーのデータ"""

    email: str = Field(max_length=320)
    name: str | None = Field(max_length=100)
    bio: str | None = Field(max_length=1000)
