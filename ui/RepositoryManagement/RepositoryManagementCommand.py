# coding: utf-8

from ui.command import ICommand
from ..WindowManager import get_main_window

from .RepositoryManagementDialog import RepositoryManagementDialog


class RepositoryManagementCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = RepositoryManagementDialog(get_main_window())
        dialog.exec()
