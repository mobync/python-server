import json
from dataclasses import dataclass
from enum import Enum


class OperationType(Enum):

    create: int = 0
    update: int = 1
    delete: int = 2

    @classmethod
    def validate(cls, operation_type):
        return type(operation_type) == str and operation_type in [cls.create.name, cls.update.name, cls.delete.name]


@dataclass
class Diff:

    ID: str = 'id'
    OWNER: str = 'owner'
    LOGICAL_CLOCK: str = 'logical_clock'
    UTC_TIMESTAMP: str = 'utc_timestamp'
    TYPE: str = 'type'
    MODEL: str = 'model'
    JSON_DATA: str = 'json_data'

    @staticmethod
    def validate(data):
        if type(data) == str:
            data = json.loads(data)

        if Diff.__validate_diff_json(data):
            return Diff.__validate_type_with_json_data(data)

        return False

    @staticmethod
    def __validate_diff_json(data: dict):

        valid = True
        field_list = [
            Diff.ID,
            Diff.OWNER,
            Diff.LOGICAL_CLOCK,
            Diff.UTC_TIMESTAMP,
            Diff.TYPE,
            Diff.MODEL,
            Diff.JSON_DATA,
        ]

        for field in field_list:
            if field in data and valid:
                valid = Diff.__validate_map()[field](data[field])
                if not valid:
                    print(valid)
            else:
                if not valid:
                    return False
                if field != Diff.JSON_DATA:
                    return False

        return valid

    @staticmethod
    def __validate_type_with_json_data(data):
        if data[Diff.TYPE] != OperationType.delete:
            return Diff.JSON_DATA in data and type(data[Diff.JSON_DATA]) == str and bool(data[Diff.JSON_DATA])
        else:
            return Diff.JSON_DATA not in data or data[Diff.JSON_DATA] is None or not bool(data[Diff.JSON_DATA])

    @staticmethod
    def __validate_map():
        return {
            Diff.ID: Diff.__validate_id,
            Diff.OWNER: Diff.__validate_owner,
            Diff.LOGICAL_CLOCK: Diff.__validate_logical_clock,
            Diff.UTC_TIMESTAMP: Diff.__validate_utc_timestamp,
            Diff.TYPE: Diff.__validate_type,
            Diff.MODEL: Diff.__validate_model,
            Diff.JSON_DATA: Diff.__validate_json_data,
        }

    @staticmethod
    def __validate_id(id):
        return type(id) == str and bool(id)

    @staticmethod
    def __validate_owner(owner):
        return type(owner) == str and bool(owner)

    @staticmethod
    def __validate_logical_clock(logical_clock):
        return type(logical_clock) == int and logical_clock >= 0

    @staticmethod
    def __validate_utc_timestamp(utc_timestamp):
        return type(utc_timestamp) == int and utc_timestamp >= 0

    @staticmethod
    def __validate_type(operation_type):
        return OperationType.validate(operation_type)

    @staticmethod
    def __validate_model(model):
        return type(model) == str and bool(model)

    @staticmethod
    def __validate_json_data(json_data):
        return type(json_data) == str or json_data is None
