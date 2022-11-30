# coding: utf-8

from typing import Union

from PySide6.QtWidgets import QMainWindow


_main_window: Union[QMainWindow, None] = None


def set_main_window(win: Union[QMainWindow, None]) -> None:
    global _main_window
    _main_window = win


def get_main_window() -> Union[QMainWindow, None]:
    return _main_window
