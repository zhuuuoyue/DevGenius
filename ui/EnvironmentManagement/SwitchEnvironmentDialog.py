# coding: utf-8

from typing import Optional

from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from zui import DialogBase

from .ProgramDirectorySelector import ProgramDirectorySelector
from .EnvironmentSelector import EnvironmentSelector


class SwitchEnvironmentDialogUI(object):

    def __init__(self, owner: QWidget):
        self.program_directory_selector = ProgramDirectorySelector(parent=owner)
        self.environment_selector = EnvironmentSelector(parent=owner)
        self.bottom_spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.program_directory_selector)
        self.layout.addWidget(self.environment_selector)
        self.layout.addSpacerItem(self.bottom_spacer)

        owner.setLayout(self.layout)


class SwitchEnvironmentDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle(u"Environment Management")
        self.setMinimumSize(QSize(600, 460))

        self._ui = SwitchEnvironmentDialogUI(self)

    @Slot(str)
    def _on_environment_button_clicked(self, text: str) -> None:
        print(text)

