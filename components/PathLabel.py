# coding: utf-8

import os
from abc import ABC, abstractmethod
from typing import Optional, Union

from PySide6.QtWidgets import QWidget, QLineEdit


class PathValidator(ABC):

    @abstractmethod
    def validate(self, path: str) -> bool:
        pass


class FilePathValidator(PathValidator):

    def validate(self, path: str) -> bool:
        return os.path.isfile(path)


class DirectoryPathValidator(PathValidator):

    def validate(self, path: str) -> bool:
        return os.path.isdir(path)


class PathLabel(QLineEdit):

    def __init__(self, parent: Optional[QWidget] = None, validator: Optional[PathValidator] = None):
        super().__init__(parent=parent)
        self.setEnabled(False)
        self.__validator: Union[PathValidator, None] = None
        self.__path: Union[str, None] = None

        self.validator = validator

    def get_validator(self) -> Union[PathValidator, None]:
        return self.__validator

    def set_validator(self, validator: Union[PathValidator, None]) -> None:
        if validator is None or isinstance(validator, PathValidator):
            self.__validator = validator
            self.__update()

    validator = property(get_validator, set_validator)

    def set_path(self, path: Union[str, None]) -> None:
        if path is None or isinstance(path, str):
            self.__path = path
            self.__update()

    def __update(self):
        if self.__path is None:
            self.setText(u"")
        else:
            self.setText(self.__path)
            if isinstance(self.__validator, PathValidator) and not self.__validator.validate(self.__path):
                self.setStyleSheet("color: red;")
            else:
                self.setStyleSheet("color: black;")


def create_file_path_label(parent: Optional[QWidget] = None) -> PathLabel:
    return PathLabel(parent=parent, validator=FilePathValidator())


def create_directory_path_label(parent: Optional[QWidget] = None) -> PathLabel:
    return PathLabel(parent=parent, validator=DirectoryPathValidator())


__all__ = [
    "PathLabel",
    "create_file_path_label",
    "create_directory_path_label",
    "PathValidator",
    "FilePathValidator",
    "DirectoryPathValidator"
]
