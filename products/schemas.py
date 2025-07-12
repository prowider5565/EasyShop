from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: int
    owner_id: int

    class Config:
        from_attributes = True


# class RemoveSchema(BaseModel):
#     owner_id: int
#     product_id: int


class UpdateSchema(BaseModel):
    owner_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class PaginationSchema(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10
