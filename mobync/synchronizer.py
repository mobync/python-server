import abc
from typing import List

from mobync import ReadFilter


class Synchronizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read(self, where: str, filters: List[ReadFilter]) -> str:
        pass

    @abc.abstractmethod
    def update(self, where: str, data_json: str) -> None:
        pass

    @abc.abstractmethod
    def validate_update(self, owner_id: str, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def create(self, where: str, data_json: str) -> None:  # todo: should receive dict?
        pass

    @abc.abstractmethod
    def validate_create(self, owner_id: str, **kwargs) -> bool:
        pass

    @abc.abstractmethod
    def delete(self, where: str, data_json: str) -> None:
        pass

    @abc.abstractmethod
    def validate_delete(self, owner_id: str, **kwargs) -> bool:
        pass
