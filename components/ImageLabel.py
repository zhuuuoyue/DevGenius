# coding: utf-8

from typing import Optional

from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QLabel


class ImageLabel(QLabel):

    def __init__(self, image_path: str, width: Optional[int] = None, height: Optional[int] = None,
                 parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        pix = QPixmap(image_path)
        if width is None:
            width = pix.width()
        if height is None:
            height = pix.height()
        pix.scaled(QSize(width, height))
        self.setPixmap(pix)
        self.setFixedSize(QSize(width, height))


__all__ = ["ImageLabel"]
