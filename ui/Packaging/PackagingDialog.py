# coding: utf-8

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget

from components import DialogBase


class PackagingDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="84454f71-3292-46f5-819e-2c3fb55a5d4f")
        self.setWindowTitle(u"Packaging")
        self.setMinimumSize(QSize(600, 400))
