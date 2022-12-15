# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .SwitchEnvironmentDialog import SwitchEnvironmentDialog


class SwitchEnvironmentCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = SwitchEnvironmentDialog(get_main_window())
        dialog.exec()
