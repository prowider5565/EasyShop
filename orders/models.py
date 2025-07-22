from datetime import datetime
from sqlalchemy import UUID, Column, Integer, ForeignKey, DateTime,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from core.settings import Base
import uuid


# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(Integer, primary_key=True)
#     customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     status = Column(String, default="Ordered")
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False)
#     # Aloqa
#     items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(String, ForeignKey("users.id"), nullable=True)  # ForeignKey qo‘shildi
    address_id = Column(Integer)

    customer = relationship("User", back_populates="orders")
    items = relationship("ItemSet", back_populates="order")

class ItemSet(Base):
    __tablename__ = "itemsets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_variant_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    order = relationship("Order", back_populates="items")

# class OrderItem(Base):
#     __tablename__ = "order_items"

#     id = Column(Integer, primary_key=True)
#     order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
#     product_variant_id = Column(Integer, ForeignKey("product_variants.id"), nullable=False)
#     quantity = Column(Integer, nullable=False)

#     # Aloqalar
#     order = relationship("Order", back_populates="items")
#     product_variant = relationship("ProductVariant")


