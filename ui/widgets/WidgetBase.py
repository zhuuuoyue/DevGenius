# coding: utf-8

from typing import Optional

from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QWidget, QStyleOption, QStyle


class WidgetBase(QWidget):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def paintEvent(self, event: QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        style: QStyle = self.style()
        style.drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
