# coding: utf-8

import os
from typing import Optional

from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtCore import QSize, Qt, QMargins, Slot, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

from .WidgetBase import WidgetBase


class SearchBarUI(object):

    def __init__(self, owner: QWidget, icon: str, text_placeholder: Optional[str] = None):
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(QMargins(1, 1, 1, 1))
        self.icon = QLabel(parent=owner)
        self.icon.setFixedSize(QSize(22, 22))
        self.icon.setPixmap(QPixmap(icon).scaled(18, 18))
        self.input = QLineEdit(parent=owner)
        self.input.setClearButtonEnabled(True)
        if text_placeholder is not None and len(text_placeholder) != 0:
            self.input.setPlaceholderText(text_placeholder)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.input)
        owner.setLayout(self.layout)
        owner.setStyleSheet(f"""SearchBar {{
        border: 1px solid gray;
        }}
        SearchBar QLabel {{
        padding: 2px;
        }}
        SearchBar QLineEdit {{
        border: none;
        }}
        """)
        owner.setFixedHeight(24)


class SearchBar(WidgetBase):

    keyword_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self._ui = SearchBarUI(owner=self, icon=f"{os.getcwd()}\\assets\\search.png",
                               text_placeholder=u"type keyword and start searching ...")

    def get_keyword(self) -> str:
        return self._ui.input.text()

    def in_searching_mode(self) -> bool:
        return len(self.get_keyword()) != 0

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._ui.input.setFocus()


__all__ = ["SearchBar"]
