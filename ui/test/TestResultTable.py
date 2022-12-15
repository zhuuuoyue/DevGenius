# coding: utf-8

import os
from typing import Optional, Union, Any

from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView

from concepts.test import TestCaseRunningResultCollection, TestCase, TestCaseRunningResult, TestCaseRunningError
from components import AdvancedTable, TableCellFormatter, TableColumnData


def create_read_only_cell(text: str) -> QTableWidgetItem:
    cell = QTableWidgetItem()
    cell.setText(text)
    cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
    return cell


class StatusFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return create_read_only_cell(data.status)


class GroupFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return create_read_only_cell(data.test_case.group)


class NameFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return create_read_only_cell(data.test_case.name)


class MessageFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return None if data.error_info is None else create_read_only_cell(data.error_info.message)


class FilenameFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        if not isinstance(data.error_info, TestCaseRunningError):
            return None
        segments = os.path.split(data.error_info.filename)
        if len(segments) < 2:
            return None
        return create_read_only_cell(segments[1])


class LineNumberFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return None if data.error_info is None else create_read_only_cell(str(data.error_info.line_number))


class FunctionFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return None if data.error_info is None else create_read_only_cell(data.error_info.function)


class AuthorFormatter(TableCellFormatter):

    def format(self, row_index: int, column_index: int, table: QTableWidget, data: TestCaseRunningResult,
               data_list: list[TestCaseRunningResult], *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        return None if data.error_info is None else create_read_only_cell(data.error_info.author)


class TestResultTable(AdvancedTable):

    __columns: list[TableColumnData] = [
        TableColumnData(StatusFormatter(), u"结果", 80),
        TableColumnData(GroupFormatter(), u"分组", 180),
        TableColumnData(NameFormatter(), u"文件名", None),
        TableColumnData(MessageFormatter(), u"错误描述", None),
        TableColumnData(FilenameFormatter(), u"出错文件", None),
        TableColumnData(LineNumberFormatter(), u"行号", 60),
        TableColumnData(FunctionFormatter(), u"出错函数", None),
        TableColumnData(AuthorFormatter(), u"作者", 80),
    ]

    selectedTestCaseChanged = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(TestResultTable.__columns, parent=parent)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.__data: TestCaseRunningResultCollection = TestCaseRunningResultCollection()

        self.pressed.connect(self.__on_selection_changed)

    def load_data(self, items: TestCaseRunningResultCollection) -> None:
        self.__data = items
        super().load_data(self.__data.data)

    def get_selected_test_case(self) -> Union[TestCase, None]:
        indexes = self.selectedIndexes()
        if len(indexes) == 0:
            return None
        index = indexes[0].row()
        return self.__data.get_item_by_index(index)

    @Slot()
    def __on_selection_changed(self) -> None:
        self.selectedTestCaseChanged.emit()
