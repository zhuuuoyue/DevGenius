# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .PackagingDialog import PackagingDialog


class PackagingCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = PackagingDialog(parent=get_main_window())
        dialog.exec()
