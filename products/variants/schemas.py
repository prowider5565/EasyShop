from pydantic import BaseModel
from typing import Optional


class VariantBase(BaseModel):
    name: str
    price: Optional[float] = None
    in_stock: Optional[int] = 0
    is_active: Optional[bool] = True


class VariantCreate(VariantBase):
    product_id: int


class VariantUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    in_stock: Optional[int]
    is_active: Optional[bool]


class VariantOut(VariantBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True
