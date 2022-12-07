# coding: utf-8

from uuid import uuid4, UUID
from enum import Enum
from typing import Optional
from abc import ABC


class CompilationConfiguration(Enum):
    """C++ solution configuration.
    """
    Debug = 0
    Release = 1
    QDebug = 2


class Identifiable(ABC):

    def __init__(self, id_: int = -1):
        self.__id = -1
        self.id = id_

    def get_id(self) -> int:
        return self.__id

    def set_id(self, id_: int) -> None:
        if isinstance(id_, int):
            self.__id = id_

    id = property(get_id, set_id)


class Repository(Identifiable):
    """Project repository information.
    """

    def __init__(self, name: str, path: str, id_: int = -1):
        super().__init__(id_)
        self.__name = ""
        self.__path = ""

        self.name = name
        self.path = path

    def get_name(self) -> str:
        return self.__name

    def set_name(self, value: str) -> None:
        if isinstance(value, str):
            self.__name = value

    name = property(get_name, set_name)

    def get_path(self) -> str:
        return self.__path

    def set_path(self, value: str) -> None:
        if isinstance(value, str):
            self.__path = value

    path = property(get_path, set_path)


class PathType(Enum):
    """Path type, including local path and remote path.
    """
    Local = 1       # 本地路径
    Remote = 2      # FTP 路径


class EnvironmentType(Enum):

    QA = 0
