# coding: utf-8

import os
from typing import Optional

from PySide6.QtCore import QSize, Slot, Qt
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,\
    QLineEdit

from concepts.test import TestCase, DbgWarnInfo
from bussiness.TestUtils import analysis_test_results
from components import DialogBase


class TestResultTable(QTableWidget):

    __columns: list[str] = [u"测试用例", u"脚本文件名", u"类型", u"任务 ID", u"文件名", u"行号", u"函数/方法", u"调试信息",
                            u"作者", u"日期"]

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setColumnCount(len(TestResultTable.__columns))
        self.setHorizontalHeaderLabels(TestResultTable.__columns)

    def remove_all_rows(self) -> None:
        while self.rowCount():
            self.removeRow(0)

    def load_data(self, items: list[TestCase]) -> None:
        self.setRowCount(len(items))
        for row, item in enumerate(items):
            self.set_cell(row, 0, item.name)
            self.set_cell(row, 1, item.js_filename)
            err = item.error
            if err is None:
                continue
            self.set_cell(row, 2, "")
            self.set_cell(row, 3, str(err.task_id))
            self.set_cell(row, 4, err.filename)
            self.set_cell(row, 5, str(err.line_number))
            self.set_cell(row, 6, err.function)
            self.set_cell(row, 7, err.message)
            self.set_cell(row, 8, err.author)

    def set_cell(self, row: int, col: int, value: str) -> None:
        cell = QTableWidgetItem()
        cell.setText(value)
        cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsSelectable & ~Qt.ItemFlag.ItemIsEditable)
        self.setItem(row, col, cell)


class AnalysisTestResultDialogUI(object):

    def __init__(self, owner: QWidget):
        self.path_title = QLabel(u"测试输出目录", parent=owner)
        self.path_input = QLineEdit(parent=owner)
        self.analysis = QPushButton(parent=owner)
        self.analysis.setText(u"分析")
        self.analysis.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.path_title)
        self.top_layout.addWidget(self.path_input)
        self.top_layout.addWidget(self.analysis)

        self.result = TestResultTable(parent=owner)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.result)

        owner.setLayout(self.layout)


class AnalysisTestResultDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="analysis_test_result")
        self.setWindowTitle(u"分析测试结果")
        self.setMinimumSize(QSize(1500, 600))
        self.__ui = AnalysisTestResultDialogUI(self)

        self.__ui.analysis.clicked.connect(self.__on_analysis_clicked)

    @Slot()
    def __on_analysis_clicked(self) -> None:
        directory = self.__ui.path_input.text()
        if not os.path.isdir(directory):
            return
        result = analysis_test_results(directory)
        self.__ui.result.load_data(result)
