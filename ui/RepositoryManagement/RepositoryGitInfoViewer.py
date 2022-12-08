# coding: utf-8

from typing import Optional, Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView

from concepts import BranchInfo
from components import WidgetBase
from bussiness import RepositoryUtils


class BranchTable(QTableWidget):

    def __init__(self, parent: Optional[QWidget] = None, *arg, **kwargs):
        super().__init__(parent=parent, *arg, **kwargs)
        columns: list[str] = [u"Current", u"Dirty", u"Local Branch", u"Remote Branch"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        self.setColumnWidth(0, 40)
        self.setColumnWidth(1, 40)
        header: QHeaderView = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

    def create_readonly_text_cell(self, row: int, col: int) -> QTableWidgetItem:
        cell = QTableWidgetItem()
        cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable)
        self.setItem(row, col, cell)
        return cell

    def append_row(self, branch: BranchInfo) -> None:
        row_index = self.rowCount()
        self.setRowCount(row_index + 1)
        header: QHeaderView = self.verticalHeader()
        header.setSectionResizeMode(row_index, QHeaderView.ResizeMode.Fixed)

        current = self.create_readonly_text_cell(row_index, 0)
        if branch.current:
            current.setText(u"*")

        dirty = self.create_readonly_text_cell(row_index, 1)
        if branch.dirty:
            dirty.setText(u"*")

        name = self.create_readonly_text_cell(row_index, 2)
        name.setText(branch.name)

        remote_name = self.create_readonly_text_cell(row_index, 3)
        if branch.remote_name is not None:
            remote_name.setText(branch.remote_name)

    def load_data(self, branches: list[BranchInfo]) -> None:
        while self.rowCount():
            self.removeRow(0)
        for branch in branches:
            self.append_row(branch)


class RepositoryGitInfoViewerUI(object):

    def __init__(self, owner: QWidget):
        self.table = BranchTable(parent=owner)

        self.table_layout = QHBoxLayout()
        self.table_layout.addWidget(self.table)

        self.group_box = QGroupBox(parent=owner)
        self.group_box.setTitle(u"Git Basic Information")
        self.group_box.setLayout(self.table_layout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.group_box)

        owner.setLayout(self.layout)


class RepositoryGitInfoViewer(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__ui = RepositoryGitInfoViewerUI(self)

    def set_repository_root_path(self, root: Union[str, None]) -> None:
        branches: list[BranchInfo] = RepositoryUtils.get_branches(root) if root is not None else []
        self.__ui.table.load_data(branches)


__all__ = ["RepositoryGitInfoViewer"]
