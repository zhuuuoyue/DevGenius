# coding: utf-8

from typing import Union, Dict

from PySide6.QtWidgets import QMainWindow, QWidget


class WindowManager(object):

    def __init__(self):
        self.main_window:  Union[QMainWindow, None] = None
        self.dialogs: Dict[str, QWidget] = {}

    def register_main_window(self, win: QMainWindow) -> None:
        self.main_window = win

    def get_main_window(self) -> Union[QMainWindow, None]:
        return self.main_window

    def register_dialog(self, name: str, widget: QWidget) -> None:
        pass


_window_manager = WindowManager()


def get_window_manager():
    return _window_manager
