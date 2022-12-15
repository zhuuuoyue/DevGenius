# coding: utf-8

from os import getcwd
from typing import Optional, Union

from PySide6.QtWidgets import QWidget, QHBoxLayout, QComboBox

from components import WidgetBase, create_directory_path_label, IconButton


class EnvironmentSwitcher(QComboBox):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.addItems(["a", "b", "-- unknown --"])


class OutputDirectoryBarUI(object):

    def __init__(self, owner: QWidget):
        self.path_label = create_directory_path_label(owner)
        self.open_directory = IconButton(button_id="open_directory", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)
        self.run_exe = IconButton(button_id="run_exe", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)
        self.remove_logs = IconButton(button_id="remove_logs", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)
        self.env_switcher = EnvironmentSwitcher(parent=owner)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.open_directory)
        self.layout.addWidget(self.run_exe)
        self.layout.addWidget(self.remove_logs)
        self.layout.addWidget(self.env_switcher)
        owner.setLayout(self.layout)


class OutputDirectoryBar(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.__ui = OutputDirectoryBarUI(self)

    def set_path(self, path: Union[str, None]) -> None:
        self.__ui.path_label.set_path(path)
