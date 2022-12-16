# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .SettingDialog import PreferencesDialog


class SettingCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = PreferencesDialog(parent=get_main_window())
        dialog.exec()
