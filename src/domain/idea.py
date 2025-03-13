from pydantic import BaseModel, Field


class Idea(BaseModel):
    """アイデアのデータ"""

    name: str = Field(max_length=100)
    description: str = Field(max_length=2000)
    tag_ids: list[int] = Field(max_length=30)
    id: int
