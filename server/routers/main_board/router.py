from fastapi import APIRouter, HTTPException
from utils.main_board_utils import get_items

router = APIRouter()


@router.get("/items/", tags=["items"])
async def retrieve_items():
    return get_items()


@router.get("/items/{item_id}", tags=["items"])
async def retrieve_item_by_id(item_id: str):
    items = get_items()
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item Not Found")
    return items[item_id]
