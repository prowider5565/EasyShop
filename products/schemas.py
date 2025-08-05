from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: int
    category_id: int
    image: Optional[str] = None

    class Config:
        from_attributes = True


# class RemoveSchema(BaseModel):
#     owner_id: int
#     product_id: int


class UpdateSchema(ProductSchema):
    owner_id: Optional[int] = None
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class PaginationSchema(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10


class BuyOderSchemas(BaseModel):
    product_id: int
    count: int
