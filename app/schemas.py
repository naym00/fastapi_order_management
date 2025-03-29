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

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = Field(None, pattern=r'^[A-Z]{3}-[0-9]{5}$', examples=['ABC-12345'], description='Format: 3 uppercase letters, hyphen, 5 digits')
    price: Optional[float] = Field(0, ge=0, description='Price must be positive if provided')
    is_offer: Optional[bool] = None
    created_at: datetime = datetime.now()
    class Config:
        orm_mode = True
    
# class Bucket(BaseModel):
#     name: str
#     price: Optional[float] = 0
#     items: Optional[list[Item]] = None
#     created_at: datetime = datetime.now()

#     @root_validator(pre=True)
#     def calculate_price(cls, values):
#         items = values.get('items')
#         if items is not None:
#             values['price'] = sum(item['price'] for item in items if item.get('price') is not None)
#         return values