from typing import List

from read_filter import ReadFilter, FilterType
from examples.no_db_example.mock_data_base import DataBase
from synchronizer import Synchronizer


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

    def update(self):
        table = self.db.get_table(where)
        if table:
            table.add_row(data_json)

    def create(self, where: str, data_json: str) -> str:
        table = self.db.get_table(where)
        if table:
            table.add_row(data_json)

    def delete(self, where: str, id: str) -> str:
        table = self.db.get_table(where)
        table.remove_row(id)

    def validate(self, diff_json: str) -> bool:
        # TODO: Validate based on your business rules
        return True

    def validate_create(self, where: str, data_json: str, uuid):
        pass
