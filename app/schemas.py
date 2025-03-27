from pydantic import BaseModel, EmailStr, Field, PositiveInt, PositiveFloat, validator, root_validator
from typing import List, Union, Optional
from datetime import datetime

class Item(BaseModel):
    name: str
    code: str = Field(..., pattern=r'^[A-Z]{3}-[0-9]{5}$')
    price: Optional[float] = 0
    is_offer: Optional[bool] = None
    created_at: datetime = datetime.now()

    @validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError(f'price should be positive!')
        return value
    class Config:
        orm_mode = True
    
class Bucket(BaseModel):
    name: str
    price: Optional[float] = 0
    items: Optional[list[Item]] = None
    created_at: datetime = datetime.now()

    @root_validator(pre=True)
    def calculate_price(cls, values):
        items = values.get('items')
        if items is not None:
            values['price'] = sum(item['price'] for item in items if item.get('price') is not None)
        return values