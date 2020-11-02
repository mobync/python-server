import abc
from typing import List

from read_filter import ReadFilter


class Synchronizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read(self, where: str, filters: List[ReadFilter]):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def create(self, where: str, data_json: str):
        pass

    @abc.abstractmethod
    def delete(self, where: str, id: str):
        pass

    @abc.abstractmethod
    def validate(self, diff_json: str) -> bool:
        pass
