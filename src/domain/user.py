from pydantic import BaseModel, Field


class User(BaseModel):
    """ユーザーのデータ"""

    email: str = Field(max_length=320)
    name: str = Field(max_length=256)
    bio: str = Field(max_length=1000)
