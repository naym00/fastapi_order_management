from pydantic import BaseModel, EmailStr, Field, PositiveInt, PositiveFloat, validator, root_validator
from typing import List, Union, Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    code: str = Field(..., pattern=r'^[A-Z]{3}-[0-9]{5}$', examples=['ABC-12345'], description='Format: 3 uppercase letters, hyphen, 5 digits')
    price: Optional[float] = Field(0, ge=0, description='Price must be positive if provided')
    is_offer: Optional[bool] = None
    created_at: datetime = datetime.now()
    class Config:
        orm_mode = True
    
class ItemCreate(ItemBase):
    pass

class Item(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = Field(None, pattern=r'^[A-Z]{3}-[0-9]{5}$', examples=['ABC-12345'], description='Format: 3 uppercase letters, hyphen, 5 digits')
    price: Optional[float] = Field(0, ge=0, description='Price must be positive if provided')
    is_offer: Optional[bool] = None
    created_at: datetime = datetime.now()
    class Config:
        orm_mode = True
    







class ChildBase(BaseModel):
    name: str
class ChildCreate(ChildBase):
    parent_id: int
class Child(ChildBase):
    parent_id: int
    class Config:
        orm_mode = True

class ParentBase(BaseModel):
    name: str
class ParentCreate(ParentBase):
    pass
class Parent(ParentBase):
    id: int
    name: str
    children: List[Child] = []
    class Config:
        orm_mode = True