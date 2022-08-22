from typing import Union
from pydantic import BaseModel
from server.enums.size_enum import SizeEnum
from server.enums.color_enum import ColorEnum
from server.enums.condition_enum import ConditionEnum


class Item(BaseModel):
    title: str
    description: Union[str, None] = None
    size: SizeEnum
    color: ColorEnum
    price: float

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    user_id: int
    title: str
    brand: str
    condition: ConditionEnum
    size: SizeEnum
    color: ColorEnum
    price: float

