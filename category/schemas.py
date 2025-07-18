from pydantic import BaseModel

class CategorySchemas(BaseModel):
    category_id: int
    name: str