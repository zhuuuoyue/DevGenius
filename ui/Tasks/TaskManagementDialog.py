# coding: utf-8

from typing import Optional, Any

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout

from zui import DialogBase, EditableList, ListItemFormatter, ListItemFilter


class TaskFilter(ListItemFilter):

    def filter(self, item: Any, keyword: str, items: list[Any] = None, index: Optional[int] = None) -> bool:
        return True


class TaskFormatter(ListItemFormatter):

    def format(self, item: Any, items: list[Any] = None, index: Optional[int] = None) -> str:
        return ""


class TaskList(EditableList):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(
            parent=parent,
            item_formatter=TaskFormatter(),
            item_filter=TaskFilter()
        )
        self.setFixedWidth(180)


class TaskInformationBlock(QGroupBox):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setTitle(u"Task Information")


class CodeBlock(QGroupBox):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setTitle(u"Commits and Branches")


class ArchiveBlock(QGroupBox):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setTitle(u"Archives")


class TaskManagementDialogUI(object):

    def __init__(self, owner: QWidget):
        self.right_layout = QVBoxLayout()
        self.task_block = TaskInformationBlock(parent=owner)
        self.right_layout.addWidget(self.task_block)
        self.code_block = CodeBlock(parent=owner)
        self.right_layout.addWidget(self.code_block)
        self.archive_block = ArchiveBlock(parent=owner)
        self.right_layout.addWidget(self.archive_block)

        self.task_list = TaskList(parent=owner)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.task_list)
        self.layout.addLayout(self.right_layout)
        owner.setLayout(self.layout)


class TaskManagementDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setWindowTitle(u"Task Management")
        self.setMinimumSize(QSize(600, 400))
        self.ui = TaskManagementDialogUI(self)
