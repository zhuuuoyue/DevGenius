# coding: utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from ..command import ICommand
from ..WindowManager import get_main_window


class AlwaysOnTopCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        win = get_main_window()
        if isinstance(win, QMainWindow):
            if "checked" in kwargs:
                checked = kwargs["checked"]
                if checked:
                    win.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
                else:
                    win.setWindowFlags(Qt.WindowType.Widget)
                win.show()
