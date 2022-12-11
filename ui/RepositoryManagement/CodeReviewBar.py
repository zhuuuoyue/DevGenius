# coding: utf-8

import os
import subprocess
from typing import Optional, Union

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout

from bussiness import Utils
from components import WidgetBase, create_file_path_label, IconButton


class RunCodeReviewButton(IconButton):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(button_id="run_code_review", icon=Utils.get_icon("run.png"), parent=parent)
        self.setStyleSheet(""".RunCodeReviewButton {
        border-radius: 0px;
        border: 1px solid #cccccc;
        }
        RunCodeReviewButton::hover {
        background-color: #cccccc;
        }
        """)
        self.triggered.connect(self.__on_triggered)

        self.__path = None
        self.__update()

    @Slot(str)
    def __on_triggered(self) -> None:
        sp = subprocess.Popen(self.__path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = sp.communicate()

    def __update(self) -> None:
        if self.__path is not None and os.path.isfile(self.__path):
            self.setEnabled(True)
        else:
            self.setEnabled(False)

    def set_path(self, path: Union[str, None]) -> None:
        if isinstance(path, str) or path is None:
            self.__path = path
            self.__update()


class CodeReviewBarUI(object):

    def __init__(self, owner: QWidget):
        self.path_label = create_file_path_label(owner)
        self.run_bat = RunCodeReviewButton(parent=owner)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.run_bat)
        owner.setLayout(self.layout)


class CodeReviewBar(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.__ui = CodeReviewBarUI(self)

    def set_path(self, path: Union[str, None]) -> None:
        self.__ui.path_label.set_path(path)
        self.__ui.run_bat.set_path(path)
