# coding: utf-8

from abc import ABC, abstractmethod


class ICommand(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        pass
