# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .TaskManagementDialog import TaskManagementDialog


class TaskManagementCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = TaskManagementDialog(parent=get_main_window())
        dialog.exec()
