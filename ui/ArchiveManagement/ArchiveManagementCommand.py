# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .ArchiveManagementDialog import ArchiveManagementDialog


class ArchiveManagementCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = ArchiveManagementDialog(parent=get_main_window())
        dialog.exec()
