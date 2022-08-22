from fastapi import APIRouter, HTTPException, Query
from fastapi_utils.cbv import cbv
from typing import List, Optional
from server.utils.items_utils import ItemManager
from server.schemas.main_board_schema import Item, ItemCreate

router = APIRouter()


@cbv(router)
class ItemCBV:
    def __init__(self):
        self.item_manager = ItemManager()

    @router.get("/items/all", response_model=List[Item])
    async def retrieve_items(self):
        return self.item_manager.retrieve_items()

    @router.get("/items/{keyword}", response_model=List[Item])
    async def retrieve_item_by_keyword(self, keyword: str):
        return self.item_manager.retrieve_item_by_keyword(keyword)

    @router.post("/items/add", response_model=Item)
    async def create_item(self, user_id: int, item: ItemCreate):
        return self.item_manager.add_items(user_id, item)

    @router.put("/items/{item_id}/update", response_model=Item)
    async def update_description(self, item_id: int, description: str):
        return self.item_manager.update_items(item_id)

    @router.delete("/items/{item_id}/delete")
    async def delete_item(self, item_id: int):
        return self.item_manager.delete_items(item_id)
