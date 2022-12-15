# coding: utf-8

from abc import ABC, abstractmethod
from typing import Any, Union, Optional

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHeaderView


class TableCellFormatter(ABC):

    @abstractmethod
    def format(self, row_index: int, column_index: int, table: QTableWidget, data: Any, data_list: list[Any],
               *args, **kwargs) -> Union[QTableWidgetItem, QWidget, None]:
        pass


class TableColumnData(object):

    def __init__(self, formatter: TableCellFormatter, title: Optional[str] = None, width: Optional[int] = None, *args,
                 **kwargs):
        self.title: Union[str, None] = title
        self.width: Union[int, None] = width
        self.formatter: TableCellFormatter = formatter


class AdvancedTable(QTableWidget):

    def __init__(self, columns: list[TableColumnData], parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__columns: list[TableColumnData] = columns
        self.__data_list: list[Any] = []

        self.setColumnCount(len(self.__columns))
        labels: list[str] = []
        header = self.horizontalHeader()
        for index, column in enumerate(self.__columns):
            labels.append(column.title)
            if isinstance(column.width, int) and column.width > 0:
                self.setColumnWidth(index, column.width)
                header.setSectionResizeMode(index, QHeaderView.ResizeMode.Fixed)
        self.setHorizontalHeaderLabels(labels)

    def remove_data(self) -> None:
        while self.rowCount():
            self.removeRow(0)
        self.__data_list = []

    def load_data(self, data_list: list[Any]) -> None:
        self.remove_data()
        self.setRowCount(len(data_list))
        for row_index, row_data in enumerate(data_list):
            for column_index, column_data in enumerate(self.__columns):
                formatter = column_data.formatter
                cell = formatter.format(
                    row_index=row_index,
                    column_index=column_index,
                    table=self,
                    data=row_data,
                    data_list=data_list
                )
                if isinstance(cell, QTableWidgetItem):
                    self.setItem(row_index, column_index, cell)
                elif isinstance(cell, QWidget):
                    self.setCellWidget(row_index, column_index, cell)

    def adjust_column_width(self) -> None:
        total_width = self.width() - self.verticalHeader().width() - self.verticalScrollBar().width()
        free_width = total_width
        free_columns = len(self.__columns)
        for column in self.__columns:
            if isinstance(column.width, int) and column.width > 0:
                free_columns -= 1
                free_width -= column.width
        if free_width <= 0 or free_columns <= 0:
            return
        expected_width = free_width // free_columns
        for index, column in enumerate(self.__columns):
            if isinstance(column.width, int) and column.width > 0:
                continue
            self.setColumnWidth(index, expected_width)


__all__ = ["TableCellFormatter", "TableColumnData", "AdvancedTable"]
