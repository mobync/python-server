from typing import List

from ReadFilter import ReadFilter, FilterType
from examples.no_db_example.mock_data_base import DataBase
from synchronizer import Synchronizer


class Implementation(Synchronizer):

    def __init__(self, db: DataBase):
        self.db = db

    def read(self, where: str, filters: List[ReadFilter]):

        filtered_data = self.db.get_table(where)

        if filters:
            for f in filters:
                if f.filter_by == FilterType.equal:
                    filtered_data = filtered_data.select_equal(**{f.field_name: f.data})
                # TODO: Create the others kinds of filters

        return filtered_data.to_json()

    def update(self):
        table = self.db.get_table(where)
        if table:
            table.add_row(data_json)

    def create(self, where: str, data_json: str):
        table = self.db.get_table(where)
        if table:
            table.add_row(data_json)

    def delete(self, where: str, uuid: str):
        table = self.db.get_table(where)
        table.remove_row(uuid)

    def validate(self):
        # Validate based on your business rules
        pass
