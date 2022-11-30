# coding: utf-8

from ui.command import ICommand
from ..WindowManager import get_main_window

from .ProjectManagementDialog import ProjectManagementDialog


class ProjectCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = ProjectManagementDialog(get_main_window())
        dialog.exec()
