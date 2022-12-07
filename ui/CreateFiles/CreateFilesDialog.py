# coding: utf-8

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QLabel, QSpacerItem,
    QSizePolicy, QTabWidget, QTextEdit, QPushButton)

from components import DialogBase


def create_title(title: str, parent: Optional[QWidget] = None) -> QLabel:
    widget = QLabel(text=title, parent=parent)
    widget.setFixedWidth(80)
    return widget


class CreateFilesDialogUI(object):

    def __init__(self, owner: QWidget):
        self.folder_layout = QHBoxLayout()
        self.folder_title = create_title(u"Destination", parent=owner)
        self.folder_layout.addWidget(self.folder_title)
        self.folder = QLineEdit(parent=owner)
        self.folder_layout.addWidget(self.folder)

        self.basename_layout = QHBoxLayout()
        self.basename_title = create_title(u"Base Name", parent=owner)
        self.basename_layout.addWidget(self.basename_title)
        self.basename = QLineEdit(parent=owner)
        self.basename_layout.addWidget(self.basename)

        self.extension_layout = QHBoxLayout()
        self.extension_title = create_title(u"File Types", parent=owner)
        self.extension_layout.addWidget(self.extension_title)
        self.header = QCheckBox(text=u"Header File (*.h)", parent=owner)
        self.extension_layout.addWidget(self.header)
        self.source = QCheckBox(text=u"Source File (*.cpp)", parent=owner)
        self.extension_layout.addWidget(self.source)
        self.extension_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.extension_layout.addSpacerItem(self.extension_spacer)

        self.preview = QTabWidget(parent=owner)
        self.header_preview = QTextEdit(parent=owner)
        self.preview.addTab(self.header_preview, u"Header")
        self.source_preview = QTextEdit(parent=owner)
        self.preview.addTab(self.source_preview, u"Source")

        self.button_layout = QHBoxLayout()
        self.spacer_before_create = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout.addSpacerItem(self.spacer_before_create)
        self.create = QPushButton(text=u"Create", parent=owner)
        self.button_layout.addWidget(self.create)
        self.cancel = QPushButton(text=u"Cancel", parent=owner)
        self.button_layout.addWidget(self.cancel)
        self.spacer_after_cancel = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout.addSpacerItem(self.spacer_after_cancel)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.folder_layout)
        self.layout.addLayout(self.basename_layout)
        self.layout.addLayout(self.extension_layout)
        self.layout.addWidget(self.preview)
        self.layout.addLayout(self.button_layout)

        owner.setLayout(self.layout)


class CreateFilesDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.setWindowTitle(u"Create Files")
        self.setMinimumSize(QSize(600, 400))
        self.ui = CreateFilesDialogUI(self)
