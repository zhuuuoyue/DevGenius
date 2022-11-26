# coding: utf-8

import os
from typing import Optional

from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from .WidgetBase import WidgetBase


class MenuButton(WidgetBase):

    triggered = Signal(str)

    def __init__(self, menu_id: str, name: str, icon: str, tooltip: Optional[str] = None,
                 parent: Optional[QWidget] = ..., *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self._icon = None
        self._layout = None
        self._title = None
        self._initialize(name, icon, tooltip)

        self._menu_id: str = menu_id

    def _initialize(self, name: str, icon: str, tooltip: Optional[str] = None):
        self.setFixedWidth(80)
        self.setFixedHeight(120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._layout = QVBoxLayout()
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(self._layout)
        self._icon = QLabel(self)
        self._layout.addWidget(self._icon)
        icon_image = QPixmap(icon)
        icon_image.scaled(30, 30)
        self._icon.setPixmap(icon_image)

        self._title = QLabel(text=name, parent=self)
        self._title.setFixedHeight(18)
        self._title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._title)
        if tooltip is not None:
            self.setToolTip(tooltip)
        self.setStyleSheet(""".MenuButton {
        border: 1px solid gray;
        border-radius: 5px;
        }
        .MenuButton::hover {
        background-color: gray;
        }
        .QLabel {
        font-family: "Microsoft YaHei";
        font-size: 15px;
        }
        """)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.triggered.emit(self._menu_id)
        event.accept()
