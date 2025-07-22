from pydantic import BaseModel
from typing import Optional

class VariantBase(BaseModel):
    name: str
    price: Optional[float] = None
    stock: Optional[int] = 0
    is_active: Optional[bool] = True

class VariantCreate(VariantBase):
    product_id: int

class VariantUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    is_active: Optional[bool]

class VariantOut(VariantBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True
