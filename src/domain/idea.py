from pydantic import BaseModel ,Field

class Idea(BaseModel):
    """アイデアのデータ"""

    name:str =Field(max_length=100)
    tags:list[int] =Field(max_length=30)
    id:int