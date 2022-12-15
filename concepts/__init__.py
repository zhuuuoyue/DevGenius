# coding: utf-8

from enum import Enum
from typing import Optional, Union
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


class BranchInfo(object):

    def __init__(self, name: str, current: Optional[bool] = None, remote_name: Optional[str] = None,
                 dirty: Optional[bool] = None):
        self.__name = None
        self.__remote_name = None
        self.__current = False
        self.__dirty = False

        self.name = name
        self.current = current
        self.remote_name = remote_name
        self.dirty = dirty

    def get_name(self) -> Union[str, None]:
        return self.__name

    def set_name(self, name: str) -> None:
        if isinstance(name, str):
            self.__name = name

    name = property(get_name, set_name)

    def get_remote_name(self) -> Union[str, None]:
        return self.__remote_name

    def set_remote_name(self, name: Union[str, None]) -> None:
        if name is None or isinstance(name, str):
            self.__remote_name = name

    remote_name = property(get_remote_name, set_remote_name)

    def get_current(self) -> bool:
        return self.__current

    def set_current(self, current: bool) -> None:
        if isinstance(current, bool):
            self.__current = current

    current = property(get_current, set_current)

    def get_dirty(self) -> bool:
        return self.__dirty

    def set_dirty(self, dirty: bool) -> None:
        if isinstance(dirty, bool):
            self.__dirty = dirty

    dirty = property(get_dirty, set_dirty)


class PathType(Enum):
    """Path type, including local path and remote path.
    """
    Local = 1       # 本地路径
    Remote = 2      # FTP 路径


class EnvironmentType(Enum):

    QA = 0
