from mobync import OperationType
from dataclasses import dataclass

from model import Model


@dataclass
class Task(Model):
    id: str
    name: str
    created_time: str
    done: bool

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __str__(self):
        return self.to_json()


@dataclass
class Diff(Model):

    id: str
    owner: str
    logical_clock: int
    utc_timestamp: int
    type: OperationType
    model: str
    json_data: str

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __str__(self):
        return self.to_json()
