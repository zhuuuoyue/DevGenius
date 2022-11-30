# coding: utf-8

from abc import ABC, abstractmethod
from typing import Optional, Any

from PySide6.QtWidgets import QWidget, QListWidget


class ListItemFormatter(ABC):

    @abstractmethod
    def format(self, item: Any, items: list[Any] = None, index: Optional[int] = None) -> str:
        pass


class DefaultListItemFormatter(ListItemFormatter):

    def format(self, item: Any, items: list[Any] = None, index: Optional[int] = None) -> str:
        return item.__str__()


class CustomList(QListWidget):

    def __init__(self, parent: Optional[QWidget] = None, formatter: Optional[ListItemFormatter] = None,
                 *args, **kwargs):
        super().__init__(parent=parent)
        self.formatter = formatter

    def load_data(self, data: list[Any]):
        if self.formatter is not None:
            f = self.formatter
        else:
            f = DefaultListItemFormatter()
        for index, item in enumerate(data):
            text = f.format(item, data, index)
            self.addItem(text)


__all__ = ["CustomList", "ListItemFormatter"]
