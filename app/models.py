from app.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    price = Column(Float, default=0.0)
    is_offer = Column(Boolean, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)

