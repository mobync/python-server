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

        return filtered_data.to_json()

    def update(self):
        pass

    def create(self):
        pass

    def delete(self):
        pass

    def validate(self):
        pass
