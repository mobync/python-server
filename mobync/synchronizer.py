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
    def validate_create(self, where: str, data_json: str, auth: str) -> bool:
        pass

    @abc.abstractmethod
    def create(self, where: str, data_json: str) -> None:  # todo: should receive dict?
        pass

    @abc.abstractmethod
    def delete(self, where: str, data_json: str) -> None:
        pass

    @abc.abstractmethod
    def validate(self, diff_json: str) -> bool:  # TODO: deprecate
        pass
