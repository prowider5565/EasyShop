from pydantic import BaseModel

class CategorySchema(BaseModel):
    category_id: int
    name: str