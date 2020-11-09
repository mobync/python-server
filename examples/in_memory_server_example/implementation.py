import json
from typing import List

from mobync import ReadFilter, FilterType
from mobync import Synchronizer

from .mock_data_base import DataBase


class Implementation(Synchronizer):

    def __init__(self, db: DataBase):
        self.db = db

    def read(self, where: str, filters: List[ReadFilter]) -> str:  # todo: change return to List[dict]

        filtered_data = self.db.get_table(where)

        if filters:
            for f in filters:
                if f.filter_by == FilterType.equal:
                    filtered_data = filtered_data.select_equal(**{f.field_name: f.data})
                if f.filter_by == FilterType.major:
                    filtered_data = filtered_data.select_larger(**{f.field_name: f.data})
                if f.filter_by == FilterType.majorOrEqual:
                    filtered_data = filtered_data.select_larger_or_equal(**{f.field_name: f.data})
                # TODO: Create the others kinds of filters

        return filtered_data.to_json()

    def update(self, where: str, data_json: str):
        data = json.loads(data_json)
        table = self.db.get_table(where)
        if table:
            id = data.pop('id')
            table.update_row(id, data)

    def create(self, where: str, data_json: str) -> str:
        table = self.db.get_table(where)
        if table:
            table.add_row(data_json)

    def delete(self, where: str, data_json: str) -> None:
        data = json.loads(data_json)
        id = data.pop('id')

        table = self.db.get_table(where)
        if table:
            table.remove_row(id)

    def __validate(self, owner_id: str, **kwargs) -> bool:
        owner = kwargs['owner']
        return owner_id == owner

    def validate_create(self, owner_id: str, **kwargs) -> bool:
        return self.__validate(owner_id, **kwargs)

    def validate_update(self, owner_id: str, **kwargs) -> bool:
        return self.__validate(owner_id, **kwargs)

    def validate_delete(self, owner_id: str, **kwargs) -> bool:
        return self.__validate(owner_id, **kwargs)
