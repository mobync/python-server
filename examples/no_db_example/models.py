from examples.common.model import Model
from dataclasses import dataclass


@dataclass
class Task(Model):
    name: str
    created_time: str
    done: bool

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __str__(self):
        return self.to_json()
