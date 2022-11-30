# coding: utf-8

from uuid import uuid4, UUID
from enum import Enum
from typing import Optional


class CompilationConfiguration(Enum):
    """C++ solution configuration.
    """
    Debug = 0
    Release = 1
    QDebug = 2


class Repository(object):
    """Project repository information.
    """

    def __init__(self, path: str, name: Optional[str] = None, repo_id: Optional[UUID] = None):
        self._name = ""
        self._path = ""
        self._id = uuid4() if repo_id is None else repo_id

        self.name = name
        self.path = path

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        if isinstance(value, str):
            self._name = value

    name = property(get_name, set_name)

    def get_path(self) -> str:
        return self._path

    def set_path(self, value: str) -> None:
        if isinstance(value, str):
            self._path = value

    path = property(get_path, set_path)

    def get_id(self) -> UUID:
        return self._id

    id = property(get_id)


class PathType(Enum):
    """Path type, including local path and remote path.
    """
    Local = 1       # 本地路径
    Remote = 2      # FTP 路径


class EnvironmentType(Enum):

    QA = 0
