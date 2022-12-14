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


class TestResultTable(QTableWidget):

    __columns: list[str] = [u"结果", u"分组", u"文件名", u"错误描述", u"出错文件", u"行号", u"出错函数", u"作者"]

    selectedTestCaseChanged = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setColumnCount(len(TestResultTable.__columns))
        self.setHorizontalHeaderLabels(TestResultTable.__columns)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.__data: TestCaseRunningResultCollection = TestCaseRunningResultCollection()

        self.pressed.connect(self.__on_selection_changed)

    def __remove_all_rows(self) -> None:
        while self.rowCount():
            self.removeRow(0)
        self.__data = []

    def load_data(self, items: TestCaseRunningResultCollection) -> None:
        self.__remove_all_rows()
        self.__data = items
        self.setRowCount(self.__data.get_count())
        for row, item in enumerate(self.__data.data):
            if item.test_case is None:
                continue
            self.__set_cell(row, 0, item.status)
            self.__set_cell(row, 1, item.test_case.group)
            self.__set_cell(row, 2, item.test_case.name)
            if item.error_info is not None:
                self.__set_cell(row, 3, item.error_info.message)
                self.__set_cell(row, 4, os.path.split(item.error_info.filename)[1])
                self.__set_cell(row, 5, str(item.error_info.line_number))
                self.__set_cell(row, 6, item.error_info.function)
                self.__set_cell(row, 7, item.error_info.author)

    def get_selected_test_case(self) -> Union[TestCase, None]:
        indexes = self.selectedIndexes()
        if len(indexes) == 0:
            return None
        index = indexes[0].row()
        return self.__data.get_item_by_index(index)

    def __set_cell(self, row: int, col: int, value: str) -> None:
        cell = QTableWidgetItem()
        cell.setText(value)
        cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row, col, cell)

    @Slot()
    def __on_selection_changed(self) -> None:
        self.selectedTestCaseChanged.emit()


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
