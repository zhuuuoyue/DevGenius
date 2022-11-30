# coding: utf-8

from typing import Any, Optional
from abc import ABC, abstractmethod

from PySide6.QtWidgets import QWidget

from .WidgetBase import WidgetBase


class ListItemFilter(ABC):

    @abstractmethod
    def filter(self, item: Any, keyword: str, items: list[Any] = None, index: Optional[int] = None) -> bool:
        pass


class AdvancedList(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)


__all__ = ["ListItemFilter", "AdvancedList"]
