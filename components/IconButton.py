# coding: utf-8

from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Slot, Signal, Qt
from PySide6.QtWidgets import QWidget, QPushButton


class IconButton(QPushButton):

    small_size: int = 18
    normal_size: int = 22
    large_size: int = 24

    triggered = Signal(str)

    def __init__(self, button_id: str, icon: str, tooltip: Optional[str] = None, size: Optional[int] = None,
                 parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.button_id = button_id
        if size is None:
            size = IconButton.normal_size
        self.setFixedSize(QSize(size, size))
        if tooltip is not None:
            self.setToolTip(tooltip)
        pixmap = QPixmap(icon)
        pixmap.scaled(QSize(size, size))
        self.setIcon(pixmap)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""IconButton {{
        border: 1px solid gray;
        border-radius: 3px;
        }}
        IconButton::hover {{
        background-color: gray;
        }}
        """)

        self.clicked.connect(self._on_clicked)

    @Slot()
    def _on_clicked(self):
        self.triggered.emit(self.button_id)


__all__ = ["IconButton"]
