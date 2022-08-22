from typing import List, Dict
from datetime import datetime
from sqlalchemy import or_
from fastapi import HTTPException, Query
from server.db_models.users.users_model import UserModel
from server.db_models.items.items_model import ItemModel
from server.schemas.main_board_schema import Item, ItemCreate
from server.database import get_db


class ItemManager:

    def __init__(self):
        self._db = next(get_db())

    def retrieve_items(self) -> List[Item]:
        return self._db.query(ItemModel).all()

    def retrieve_item_by_keyword(self, keyword: str) -> List[Item]:
        keyword_filter = f"%{keyword}%"
        results = self._db.query(ItemModel).filter(
            or_(ItemModel.title.like(keyword_filter),
                ItemModel.description.like(keyword_filter)
                )
        )
        return results.all()

    def retrieve_main_board(self, filters: Dict):
        pass



    def add_items(self, user_id: int, item: ItemCreate) -> Item:
        db_item = ItemModel(
            owner_id=user_id,
            title=item.title,
            brand=item.brand,
            condition=item.condition.value,
            size=item.size.value,
            color=item.color.value,
            price=item.price,
            upload_date=datetime.now()
        )
        self._db.add(db_item)
        self._db.commit()
        self._db.refresh(db_item)
        return db_item

    def update_item_description(self, item_id: int, description: str) -> Item:
        db_item = self._db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail="Item Not Found")
        db_item.description = description
        self._db.add(db_item)
        self._db.commit()
        self._db.refresh(db_item)
        return db_item

    def delete_items(self, item_id: int):
        db_user = self._db.query(ItemModel).filter(ItemModel.id == item_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User Not Found")
        self._db.query(ItemModel).filter(ItemModel.id == item_id).delete(synchronize_session=False)
        self._db.commit()
        self._db.refresh()
        return "User has been deleted successfully"

