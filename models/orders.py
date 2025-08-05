from datetime import datetime
from enum import Enum as E
from sqlalchemy import Enum, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from core.database import Base


class OrderStatus(E):
    Ordered = "Ordered"
    Paid = "Paid"
    Pending = "Pending"
    Delivered = "Delivered"
    Cancelled = "Cancelled"



class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(
        String, ForeignKey("users.id"), nullable=True
    )  # ForeignKey qo‘shildi
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    status = Column(Enum(OrderStatus), default="Ordered", nullable=True)

    customer = relationship("User", back_populates="orders")
    items = relationship("ItemSet", back_populates="order")


class ItemSet(Base):
    __tablename__ = "itemsets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_variant_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    order = relationship("Order", back_populates="items")

