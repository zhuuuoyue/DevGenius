# coding: utf-8

from typing import Optional

from PySide6.QtGui import QPixmap, QMouseEvent
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

from components.WidgetBase import WidgetBase


class ImageButtonUI(object):

    def __init__(self, owner: QWidget, icon: str, name: str, tooltip: str, selector: str):
        owner.setFixedWidth(80)
        owner.setFixedHeight(120)
        owner.setCursor(Qt.CursorShape.PointingHandCursor)

        self.icon = QLabel(parent=owner)
        self.icon.setPixmap(QPixmap(icon).scaled(QSize(72, 90)))

        self.title = QLabel(text=name, parent=owner)
        self.title.setFixedHeight(18)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(4)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.title)
        owner.setLayout(self.layout)

        if tooltip is not None:
            owner.setToolTip(tooltip)
        owner.setStyleSheet(f"""{selector} {{
        border: 1px solid gray;
        border-radius: 5px;
        }}
        {selector}::hover {{
        background-color: gray;
        }}
        .QLabel {{
        font-family: "Microsoft YaHei";
        font-size: 15px;
        }}
        """)


class ImageButton(WidgetBase):

    clicked = Signal(str)

    def __init__(self, button_id: str, name: str, icon: str, tooltip: Optional[str] = None,
                 parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.ui = ImageButtonUI(self, icon=icon, name=name, tooltip=tooltip, selector="ImageButton")
        self.button_id: str = button_id

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.clicked.emit(self.button_id)
        event.accept()


__all__ = ["ImageButton"]
