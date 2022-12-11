# coding: utf-8

from ..command import ICommand
from ..WindowManager import get_main_window

from .CreateFilesDialog import CreateFilesDialog


class CreateFilesCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = CreateFilesDialog(get_main_window())
        dialog.exec()
