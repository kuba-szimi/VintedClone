from fastapi import HTTPException, Query
from server.database import get_db
from server.db_models.items.items_model import ItemModel
from server.schemas.main_board_schema import Item, ItemCreate
from typing import List, Dict


class MainBoard:

    PAGINATION_FILTERS = ("page", "page_size")

    def __init__(self, filters: Dict):
        self._db = next(get_db())
        self.value_filters = self._get_value_filters(filters=filters)
        self.pagination_filters = self._get_pagination_filters(filters=filters)
        self.query: Query = self.get_filtered_query()

    def get_filtered_query(self) -> Query:
        query = self._db.query(ItemModel)
        return self._apply_filters(query)

    def _get_value_filters(self, filters: Dict) -> Dict:
        return {
            filter_name: filter_value
            for filter_name, filter_value in filters.items()
            if filter_name not in self.PAGINATION_FILTERS
        }

    def _get_pagination_filters(self, filters: Dict) -> Dict:
        return {
            filter_name: filter_value
            for filter_name, filter_value in filters.items()
            if filter_name in self.PAGINATION_FILTERS
        }

    def _apply_filters(self, query: Query) -> Query:
        for filter_name, filter_value in self.value_filters.items():
            if filter_name == "size":
                query = query.filter(ItemModel.size == filter_value)
            elif filter_name == "color":
                query = query.filter(ItemModel.color == filter_value)
            elif filter_name == "condition":
                query = query.filter(ItemModel.condition == filter_value)
            elif filter_name == "brand":
                query = query.filter(ItemModel.brand == filter_value)
        return query

    def _apply_pagination(self, query: Query) -> Query:
        offset = (self.pagination_filters["page"]-1) * self.pagination_filters["page_size"]
        return query.order_by(ItemModel.id).offset(offset).limit(self.pagination_filters["page_size"])

    def select_count(self) -> int:
        return self.query.count()

    def select_data(self) -> List[Item]:
        query = self._apply_pagination(self.query)
        return query.all()


