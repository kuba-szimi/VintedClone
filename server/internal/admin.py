from fastapi import APIRouter, HTTPException
from server.schemas.main_board_schema import Item

router = APIRouter()


@router.post("/admin/")
async def update_admin():
    pass
