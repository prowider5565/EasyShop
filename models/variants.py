from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from core.database import Base
from models.products import Product  # 🟢 import qilamiz


class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    product = relationship("Product", back_populates="variants")


print("Variant model loaded successfully")  # Debug maqsadida qo'shildi
