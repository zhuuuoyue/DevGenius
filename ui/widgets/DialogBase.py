# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QDialog


class DialogBase(QDialog):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
