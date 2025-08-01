from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship

from core.database import Base
from models import variants


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    products = relationship("Product", back_populates="owner")
    orders = relationship("Order", back_populates="customer")
    variants = relationship(
        "Variant", back_populates="owner", cascade="all, delete-orphan"
    )
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
