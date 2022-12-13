# coding: utf-8

from ..command import ICommand

from .AnalysisTestResultDialog import AnalysisTestResultDialog

from ..WindowManager import get_main_window


class AnalysisTestResultCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = AnalysisTestResultDialog(parent=get_main_window())
        dialog.exec()
