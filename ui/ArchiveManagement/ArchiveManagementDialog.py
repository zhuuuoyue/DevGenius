# coding: utf-8

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QWidget, QLabel, QLineEdit, QCheckBox, QTableWidget,
                               QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy)

from components import DialogBase, WidgetBase


class FilterWidgetUI(object):

    def __init__(self, owner: QWidget):
        label_width = 60

        self.keyword_label = QLabel(text=u"Keyword", parent=owner)
        self.keyword_label.setFixedWidth(label_width)

        self.keyword_input = QLineEdit(parent=owner)
        self.keyword_input.setClearButtonEnabled(True)

        self.keyword_layout = QHBoxLayout()
        self.keyword_layout.addWidget(self.keyword_label)
        self.keyword_layout.addWidget(self.keyword_input)

        self.fields_label = QLabel(text=u"Fields", parent=owner)
        self.fields_label.setFixedWidth(label_width)

        self.fields_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)

        self.fields_layout = QHBoxLayout()
        self.fields_layout.addWidget(self.fields_label)
        self.fields_layout.addSpacerItem(self.fields_spacer)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.keyword_layout)
        self.layout.addLayout(self.fields_layout)

        owner.setLayout(self.layout)


class FilterWidget(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.ui = FilterWidgetUI(self)


class ArchiveTable(QTableWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        columns = [u"Filename", u"Size", u"Operators"]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)


class ArchiveManagementDialogUI(object):

    def __init__(self, owner: QWidget):
        self.filter = FilterWidget(parent=owner)
        self.table = ArchiveTable(parent=owner)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.filter)
        self.layout.addWidget(self.table)
        owner.setLayout(self.layout)


class ArchiveManagementDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="753017fe-41cd-49c7-8877-a737595ed4cc")
        self.setWindowTitle(u"Archive Management")
        self.setMinimumSize(QSize(600, 400))
        self.ui = ArchiveManagementDialogUI(self)
