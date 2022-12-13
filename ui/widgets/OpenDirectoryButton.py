# coding: utf-8

import os
from typing import Optional, Union

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from bussiness.Utils import get_icon
from components import IconButton


class OpenDirectoryButton(IconButton):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(button_id="open_directory", icon=get_icon("folder.png"), parent=parent)
        self.__path = None

        self.triggered.connect(self.__on_triggered)

        self.__update()

    def set_path(self, path: Union[str, None]) -> None:
        if path is None or isinstance(path, str):
            self.__path = path
            self.__update()

    @Slot(str)
    def __on_triggered(self) -> None:
        line = f"start explorer.exe {self.__path}".replace("\\\\", "\\")
        print(line)
        os.system(line)

    def __update(self) -> None:
        enabled = False
        if isinstance(self.__path, str):
            enabled = os.path.isdir(self.__path)
        self.setEnabled(enabled)
