from typing import List

from examples.common.model import Model


class Table:

    item_list: list
    item_type: type

    def __init__(self, item_list: list):
        self.item_type = Model
        if item_list:
            self.item_list = item_list
        else:
            self.item_list = list()

        for item in item_list:
            if not issubclass(type(item), Model):
                raise Warning('Incorrect table item type, expected {}, got {}'.format(self.item_type, type(item)))

    def select_equal(self, **kwargs):

        selected_items = list()
        for k in kwargs.keys():
            if k not in self.item_type.__dataclass_fields__.values():
                return []

        for item in self.item_list:
            valid = True
            for k in kwargs.keys():
                attribute = getattr(item, k)
                if attribute != kwargs[k]:
                    valid = False
                    break
            if valid:
                selected_items.append(item)

        return Table(selected_items)

    def list_table(self):
        return self.item_list


class DataBase:

    table_dict: dict

    def __init__(self):
        self.table_dict = dict()

    def get_table(self, table_name):
        if table_name in self.table_dict:
            return self.table_dict[table_name]
        else:
            return Table([])

    def add_table(self, table_name: str, items: List[Model]):
        if table_name not in self.table_dict:
            table = Table(items)
            self.table_dict[table_name] = table
        else:
            raise Warning('Tried to add repeated table {}'.format(table_name))

