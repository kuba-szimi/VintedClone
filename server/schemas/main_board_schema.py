from typing import Union
from pydantic import BaseModel
from server.enums.size_enum import SizeEnum
from server.enums.color_enum import ColorEnum


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: SizeEnum
    color: ColorEnum
    price: float
