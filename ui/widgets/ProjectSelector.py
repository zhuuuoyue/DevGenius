# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QComboBox

from concepts import Repository
from bussiness import get_repositories


class ProjectSelector(QComboBox):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.repositories = get_repositories()
        self.load_data()

    def load_data(self) -> None:
        for repository in self.repositories:
            if len(repository.name) == 0:
                text = repository.path
            else:
                text = f"{repository.name}[ {repository.path} ]"
            self.addItem(text)

    def get_current_project(self) -> Repository:
        index = self.currentIndex()
        return self.repositories[index]


__all__ = ["ProjectSelector"]
