from pydantic import BaseModel
from typing import List

class OrderItemSchema(BaseModel):
    product_variant_id: int
    quantity: int


class CreateOrderSchema(BaseModel):
    orders: List[OrderItemSchema]
    address_id: int
