# coding: utf-8

import os
from typing import Optional, Union

from PySide6.QtCore import QSize, Slot, Signal, Qt, QItemSelection
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,\
    QLineEdit, QAbstractItemView

from concepts.test import TestCase, TestCaseRunningError, TestCaseRunningResultCollection
from bussiness.TestUtils import parse_test_results
from components import DialogBase, PathLabel, DirectoryPathValidator

from ..widgets import OpenDirectoryButton
from .TestResultTable import TestResultTable


class AnalysisTestResultDialogUI(object):

    def __init__(self, owner: QWidget):
        self.path_title = QLabel(u"测试输出目录", parent=owner)
        self.path_input = QLineEdit(parent=owner)
        self.path_input.setFixedHeight(22)
        self.path_input.setText(r"E:\gap\bin\x64Q_Debug\Logs\2022.12.14(11h10m24s)")
        self.analysis = QPushButton(parent=owner)
        self.analysis.setText(u"分析")
        self.analysis.setFixedSize(QSize(60, 24))
        self.analysis.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.path_title)
        self.top_layout.addWidget(self.path_input)
        self.top_layout.addWidget(self.analysis)

        self.result = TestResultTable(parent=owner)

        self.directory = PathLabel(parent=owner, validator=DirectoryPathValidator())
        self.open = OpenDirectoryButton(parent=owner)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.directory)
        self.bottom_layout.addWidget(self.open)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.result)
        self.layout.addLayout(self.bottom_layout)

        owner.setLayout(self.layout)


class AnalysisTestResultDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="analysis_test_result")
        self.setWindowTitle(u"分析测试结果")
        self.setMinimumSize(QSize(1500, 600))
        self.__ui = AnalysisTestResultDialogUI(self)

        self.__ui.analysis.clicked.connect(self.__on_analysis_clicked)
        self.__ui.result.selectedTestCaseChanged.connect(self.__on_selection_changed)

    @Slot()
    def __on_analysis_clicked(self) -> None:
        directory = self.__ui.path_input.text()
        if not os.path.isdir(directory):
            return
        result = parse_test_results(directory)
        self.__ui.result.load_data(result)

    @Slot()
    def __on_selection_changed(self) -> None:
        test_case = self.__ui.result.get_selected_test_case()
        if test_case is None:
            self.__ui.directory.set_path(None)
            self.__ui.open.set_path(None)
        # else:
        #     self.__ui.directory.set_path(test_case.directory)
        #     self.__ui.open.set_path(test_case.directory)
