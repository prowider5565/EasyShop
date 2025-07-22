from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    in_stock = Column(Integer, default=0, nullable=False)

    owner = relationship("User", back_populates="products")
    category = relationship("Category", back_populates="products")
    
    variants = relationship("Variant", back_populates="product", cascade="all, delete-orphan")
