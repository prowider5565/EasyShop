from pydantic import BaseModel
from typing import List

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class CreateOrderSchema(BaseModel):
    items: List[OrderItemSchema]
