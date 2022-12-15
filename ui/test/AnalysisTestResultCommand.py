# coding: utf-8

from ..command import ICommand

from .TestWindow import TestWindow

from ..WindowManager import get_main_window


class AnalysisTestResultCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        if True:
            win = TestWindow(parent=get_main_window())
            win.show()
