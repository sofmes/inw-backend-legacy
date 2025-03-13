from pydantic import BaseModel, Field


class Tag(BaseModel):
    """タグのデータ"""

    name: str = Field(max_length=100)
    id: int
