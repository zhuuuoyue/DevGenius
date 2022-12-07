# coding: utf-8

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget

from components import DialogBase


class PreferencesDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="83e4862a-504c-481d-8a56-ba976863236e")
        self.setWindowTitle(u"Preferences")
        self.setMinimumSize(QSize(600, 400))
