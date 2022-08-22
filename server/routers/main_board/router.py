from fastapi import APIRouter, HTTPException, Query
from fastapi_utils.cbv import cbv
from typing import List, Optional
from server.utils.items_utils import ItemManager
from server.utils.main_board_utils import MainBoard
from server.schemas.main_board_schema import Item, ItemCreate
from server.enums.size_enum import SizeEnum
from server.enums.color_enum import ColorEnum
from server.enums.condition_enum import ConditionEnum
from server.enums.main_board.sort_by_enum import SortByEnum


router = APIRouter()


@cbv(router)
class MainBoardCBV:
    def __init__(self):
        self.item_manager = ItemManager()

    @router.get("/main-board")
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
            sort_by: Optional[SortByEnum] = Query(
                default="Brand",
                title="Sort by",
                description="Pick a sort by"
            )
    ):
        filters = {
            filter_name: filter_value
            for filter_name, filter_value in vars().items()
            if filter_name != "self" and filter_value is not None
        }
        main_board_reader = MainBoard(filters)
        return {
            "data": main_board_reader.select_data(),
            "count": main_board_reader.select_count()
        }