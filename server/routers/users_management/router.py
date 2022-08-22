from fastapi import APIRouter, HTTPException, Query
from fastapi_utils.cbv import cbv
from typing import List, Dict, Union
from server.utils.users_utils import UserManager
from server.schemas.users_schema import UserCreate, User

router = APIRouter()


@cbv(router)
class UserCBV:

    def __init__(self):
        self.users_manager = UserManager()

    @router.get("/users/", response_model=List[User])
    async def retrieve_users(self):
        return self.users_manager.retrieve_users()

    @router.get("/users/{user_id}", response_model=User)
    async def retrieve_user_by_id(self, user_id: int):
        db_user = self.users_manager.retrieve_users_by_id(user_id)

        return db_user

    @router.post("/users/register")
    async def create_user(self, user: UserCreate):
        db_user = self.users_manager.create_user(user)
        return {
            "message": "User successfully created",
            "result": {
                "email": db_user.email,
                "nickname": db_user.nickname,
                "location": db_user.location
            }
        }

    @router.put("/users/{user_id}/update/")
    async def update_user_bio(self, user_id: int, description: str):
        db_user = self.users_manager.update_item_description(user_id, description)
        return {
            "message": "User successfully updated",
            "result": db_user
        }

    @router.delete("/users/{user_id}/delete/")
    async def delete_user(self, user_id: int):
        return self.users_manager.delete_user(user_id)
