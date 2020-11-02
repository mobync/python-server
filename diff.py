import json
from dataclasses import dataclass
from enum import Enum

from examples.common.model import Model  # TODO: change model folder


class OperationType(Enum):

    create: int = 0
    update: int = 1
    delete: int = 2

    @classmethod
    def validate(cls, operation_type):
        return type(operation_type) == int and cls.create <= operation_type <= cls.delete


@dataclass
class Diff(Model):

    id: str
    owner: str
    logical_clock: int
    utc_timestamp: int
    type: OperationType
    model: str
    json_data: str

    __ID: str = 'id'
    __OWNER: str = 'owner'
    __LOGICAL_CLOCK: str = 'logical_clock'
    __UTC_TIMESTAMP: str = 'utc_timestamp'
    __TYPE: str = 'type'
    __MODEL: str = 'model'
    __JSON_DATA: str = 'json_data'

    @staticmethod
    def validate_diff_json(data):
        if type(data) == str:
            data = json.loads(data)

        valid = True
        field_list = [
            Diff.__ID,
            Diff.__OWNER,
            Diff.__LOGICAL_CLOCK,
            Diff.__UTC_TIMESTAMP,
            Diff.__TYPE,
            Diff.__MODEL,
            Diff.__JSON_DATA,
        ]

        for field in field_list:
            if field in data and valid:
                valid = Diff.__validate_map()[field](data[Diff.__ID])
            else:
                if not valid:
                    return False
                if field != Diff.json_data:
                    return False

        return valid

    @staticmethod
    def __validate_map():
        return {
            Diff.__ID: Diff.__validate_id,
            Diff.__OWNER: Diff.__validate_owner,
            Diff.__LOGICAL_CLOCK: Diff.__validate_logical_clock,
            Diff.__UTC_TIMESTAMP: Diff.__validate_utc_timestamp,
            Diff.__TYPE: Diff.__validate_type,
            Diff.__MODEL: Diff.__validate_model,
            Diff.__JSON_DATA: Diff.__validate_json_data,
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

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __str__(self):
        return self.to_json()
