# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .PreferencesDialog import PreferencesDialog


class PreferencesCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = PreferencesDialog(parent=get_main_window())
        dialog.exec()
