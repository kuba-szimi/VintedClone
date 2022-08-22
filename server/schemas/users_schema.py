from typing import List, Union
from pydantic import BaseModel
from server.schemas.main_board_schema import Item


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    nickname: str
    password: str
    location: str


class UserView(UserBase):
    nickname: str
    #is_active: bool
    location: str
    bio: Union[str, None] = None
    items: List[Item] = []


class User(UserBase):
    id: int
    #is_active: bool
    location: str
    bio: Union[str, None] = None
    items: List[Item] = []

    class Config:
        orm_mode = True
