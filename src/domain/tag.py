from pydantic import BaseModel ,Field

class Tag(BaseModel):
    """タグのデータ"""
    name:str = Field(max_length=256)
    id:int