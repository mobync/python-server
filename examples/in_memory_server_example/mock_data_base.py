import json
import warnings
from typing import List, Dict

from .model import Model


class Table:

    item_list: list
    item_parent: type
    item_class: type

    def __init__(self, item_class: type, item_list: list):
        self.item_parent = Model
        self.item_class = item_class
        if item_list:
            self.item_list = item_list
        else:
            self.item_list = list()

        for item in item_list:
            if not issubclass(type(item), Model):
                raise Warning('Incorrect table item type, expected {}, got {}'.format(self.item_parent, type(item)))

    def select_equal(self, **kwargs):

        selected_items = list()
        for k in kwargs.keys():
            if k not in self.item_class.__dataclass_fields__:
                return Table(self.item_class, [])

        for item in self.item_list:
            valid = True
            for k in kwargs.keys():
                attribute = getattr(item, k)
                if attribute != kwargs[k]:
                    valid = False
                    break
            if valid:
                selected_items.append(item)

        return Table(self.item_class, selected_items)

    def select_larger(self, **kwargs):

        selected_items = list()
        for k in kwargs.keys():
            if k not in self.item_class.__dataclass_fields__:
                return Table(self.item_class, [])

        for item in self.item_list:
            valid = True
            for k in kwargs.keys():
                attribute = getattr(item, k)
                if not attribute > kwargs[k]:
                    valid = False
                    break
            if valid:
                selected_items.append(item)

        return Table(self.item_class, selected_items)

    def select_larger_or_equal(self, **kwargs):

        selected_items = list()
        for k in kwargs.keys():
            if k not in self.item_class.__dataclass_fields__:
                return Table(self.item_class, [])

        for item in self.item_list:
            valid = True
            for k in kwargs.keys():
                attribute = getattr(item, k)
                if not attribute >= kwargs[k]:
                    valid = False
                    break
            if valid:
                selected_items.append(item)

        return Table(self.item_class, selected_items)

    def list_table(self):
        return self.item_list

    def to_json(self):
        resp = [m.to_dict() for m in self.list_table()]
        return json.dumps(resp)

    def add_row(self, data_json: str):
        args = json.loads(data_json)
        new_row = self.item_class(**args)
        self.item_list.append(new_row)

    def remove_row(self, id):
        new_list = list()
        for item in self.item_list:
            if item.id != id:
                new_list.append(item)

        self.item_list = new_list


class DataBase:

    table_dict: Dict[str, Table]

    def __init__(self):
        self.table_dict = dict()

    def get_table(self, table_name):
        if table_name in self.table_dict:
            return self.table_dict[table_name]
        else:
            warnings.warn('table {} not found on database'.format(table_name), RuntimeWarning)
            return None

    def add_table(self, table_name: str, items: List[Model], item_class: type):
        if table_name not in self.table_dict:
            table = Table(item_class, items)
            self.table_dict[table_name] = table
        else:
            raise Warning('Tried to add repeated table {}'.format(table_name))

    def to_json(self):
        resp = dict()
        for key in self.table_dict.keys():
            resp[key] = json.loads(self.table_dict[key].to_json())

        return json.dumps(resp)
