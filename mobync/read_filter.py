from enum import Enum


class FilterType(Enum):
    equal = 0
    major = 1
    minor = 2
    majorOrEqual = 3
    minorOrEqual = 4


class ReadFilter:
    field_name: str
    filter_by: FilterType
    data: any

    def __init__(self, field_name: str, filter_by: FilterType, data: any):
        self.field_name = field_name
        self.filter_by = filter_by
        self.data = data
