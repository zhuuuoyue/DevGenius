# coding: utf-8

from os import getcwd
from typing import Optional, Union

from PySide6.QtWidgets import QWidget, QHBoxLayout

from components import WidgetBase, create_directory_path_label, IconButton


class SolutionDirectoryBarUI(object):

    def __init__(self, owner: QWidget):
        self.path_label = create_directory_path_label(owner)
        self.create_solution = IconButton(button_id="open_directory", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)
        self.update_solution = IconButton(button_id="run_exe", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)
        self.open_vs15 = IconButton(button_id="remove_logs", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)
        self.open_vs19 = IconButton(button_id="remove_logs", icon=f"{getcwd()}\\assets\\mail.png", parent=owner)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.create_solution)
        self.layout.addWidget(self.update_solution)
        self.layout.addWidget(self.open_vs15)
        self.layout.addWidget(self.open_vs19)
        owner.setLayout(self.layout)


class SolutionDirectoryBar(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.__ui = SolutionDirectoryBarUI(self)

    def set_path(self, path: Union[str, None]) -> None:
        self.__ui.path_label.set_path(path)
