# coding: utf-8

from typing import Union, Optional

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from .WidgetBase import WidgetBase


class FormRowInfo(object):

    __default_width: int = 60

    def __init__(self,
                 width: Optional[int] = None,
                 required: Optional[bool] = None,
                 title: Optional[str] = None,
                 value: Optional[QWidget] = None,
                 shown: Optional[bool] = None,
                 tooltip: Optional[str] = None):
        self.width: Union[int, None] = width
        self.required: Union[bool, None] = required
        self.title: Union[str, None] = title
        self.value: Union[QWidget, None] = value
        self.shown: Union[bool, None] = shown
        self.tooltip: Union[str, None] = tooltip


class FormRow(WidgetBase):

    def __init__(self, data: FormRowInfo, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__layout = QHBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(8)

        self.__title = QLabel(data.title, parent=self)
        self.__title.setFixedWidth(60)
        self.__layout.addWidget(self.__title)

        self.__value = data.value if isinstance(data.value, QWidget) else QWidget(parent=self)
        self.__layout.addWidget(self.__value)

        self.setLayout(self.__layout)


class Form(WidgetBase):

    def __init__(self, data: list[FormRowInfo], parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__data: list[FormRowInfo] = data
        self.__rows: list[FormRow] = []

        self.__layout = None

        self.load_data(self.__data)

    def load_data(self, data: list[FormRowInfo]) -> None:
        self.__rows.clear()
        self.__layout = QVBoxLayout()
        self.__layout.setSpacing(6)
        self.__layout.setContentsMargins(4, 4, 4, 4)
        for item in data:
            row = FormRow(item, self)
            self.__layout.addWidget(row)
            self.__rows.append(row)
        self.setLayout(self.__layout)


__all__ = ["Form", "FormRow", "FormRowInfo"]
