from fastapi import APIRouter, HTTPException, Query
from fastapi_utils.cbv import cbv
from typing import List, Optional
from server.utils.items_utils import ItemManager
from server.utils.main_board_utils import MainBoard
from server.schemas.main_board_schema import Item, ItemCreate
from server.enums.size_enum import SizeEnum
from server.enums.color_enum import ColorEnum
from server.enums.condition_enum import ConditionEnum

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

    @router.get("/items/main-board")
    def retrieve_main_board(
            self,
            page: int = Query(
                default=1,
                title="Page number",
                description="Type a page number"
            ),
            page_size: int = Query(
                default=20,
                le=100,
                title="Page size",
                description="Type a page size"
            ),
            size: Optional[SizeEnum] = Query(
                default=None,
                title="Size",
                description="Filter by size of the product"
            ),
            color: Optional[ColorEnum] = Query(
                default=None,
                title="Color",
                description="Filter by color of the product"
            ),
            condition: Optional[ConditionEnum] = Query(
                default=None,
                title="Condition",
                description="Filter by condition of the product"
            ),
            brand: Optional[str] = Query(
                default=None,
                title="Brand",
                description="Filter by the brand of product"
            ),
    ):
        filters = {
            filter_name: filter_value
            for filter_name, filter_value in vars()
            if filter_name != "self" and filter_value is not None
        }
        main_board_reader = MainBoard(filters)
        return {
            "data": main_board_reader.select_data(),
            "count": main_board_reader.select_count()
        }

    @router.post("/items/add", response_model=Item)
    async def create_item(self, user_id: int, item: ItemCreate):
        return self.item_manager.add_items(user_id, item)

    @router.put("/items/{item_id}/update", response_model=Item)
    async def update_description(self, item_id: int, description: str):
        return self.item_manager.update_items(item_id)

    @router.delete("/items/{item_id}/delete")
    async def delete_item(self, item_id: int):
        return self.item_manager.delete_items(item_id)
