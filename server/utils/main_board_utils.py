from server.db_models.users.users_model import User
from server.db_models.items.items_model import Item
from server.database import get_db
from typing import List, Dict


class ItemManager:

    def __init__(self):
        self._db = next(get_db())

    def retrieve_items(self) -> List[Item]:
        return self._db.query(Item).all()

    def add_items(self, items_data: Dict):
        #to be finished
        self._db.insert()


def get_items():
    return {
        "1": {"item_name": "Blazer", "item_color": "Grey", "item_size": "L"},
        "2": {"item_name": "Chino", "item_color": "Navy", "item_size": "XL"}
    }