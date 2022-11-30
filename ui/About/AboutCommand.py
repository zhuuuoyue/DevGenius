# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .AboutDialog import AboutDialog


class AboutCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = AboutDialog(parent=get_main_window())
        dialog.exec()
