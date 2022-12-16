# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout

from concepts.test import TestCaseRunningResultCollection
from components import Form, FormRowInfo, PathLabel, FilePathValidator, DirectoryPathValidator


class TestRunningInfoPanelUI(object):

    def __init__(self, owner: QWidget):
        self.output_directory = PathLabel(parent=owner, validator=DirectoryPathValidator())
        self.ini_filename = PathLabel(parent=owner, validator=FilePathValidator())
        self.html_filename = PathLabel(parent=owner, validator=FilePathValidator())
        rows = [
            FormRowInfo(
                title=u"输出目录",
                value=self.output_directory
            ),
            FormRowInfo(
                title=u"HTML",
                value=self.html_filename
            ),
            FormRowInfo(
                title=u"INI",
                value=self.ini_filename
            )
        ]
        self.central_widget = Form(rows, owner)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central_widget)
        owner.setLayout(self.layout)


class TestRunningInfoPanel(QGroupBox):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent=parent)
        self.setTitle(u"运行基本信息")
        self.__ui = TestRunningInfoPanelUI(self)

    def set_data(self, data: Optional[TestCaseRunningResultCollection]) -> None:
        if data is None:
            self.__ui.output_directory.set_path(None)
            self.__ui.ini_filename.set_path(None)
            self.__ui.html_filename.set_path(None)
        else:
            self.__ui.output_directory.set_path(data.output_directory)
            self.__ui.ini_filename.set_path(data.ini_filename)
            self.__ui.html_filename.set_path(data.html_filename)
