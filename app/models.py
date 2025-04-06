from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(10), nullable=False, unique=True)
    price = Column(Float, default=0.0)
    is_offer = Column(Boolean, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)





class Parent(Base):
    __tablename__ = 'parents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    
    # Relationship to children
    children = relationship('Child', back_populates='parent', lazy='joined')

class Child(Base):
    __tablename__ = 'children'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey('parents.id', ondelete='CASCADE'))
    
    # Relationship to parent
    parent = relationship('Parent', back_populates='children')