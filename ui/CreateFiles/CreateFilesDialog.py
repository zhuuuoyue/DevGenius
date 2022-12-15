# coding: utf-8

import os
from typing import Optional, Tuple, Union

from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QLabel, QSpacerItem,
    QSizePolicy, QTabWidget, QTextEdit, QPushButton, QMessageBox)

from bussiness import CreationUtils
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
        self.header_preview.setText("""// Owner: 
// Co-Owner: 

#pragma once

""")
        self.preview.addTab(self.header_preview, u"Header")
        self.source_preview = QTextEdit(parent=owner)
        self.source_preview.setText("""// Owner: 
// Co-Owner: 

#include ".h"

""")
        self.preview.addTab(self.source_preview, u"Source")

        self.button_layout = QHBoxLayout()
        self.spacer_before_create = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout.addSpacerItem(self.spacer_before_create)
        self.create = QPushButton(text=u"Create", parent=owner)
        self.create.setEnabled(False)
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
        super().__init__(parent=parent, dialog_id="46d861c9-a8b7-440f-8a3f-929288551787")
        self.setWindowTitle(u"Create Files")
        self.setMinimumSize(QSize(600, 400))
        self.ui = CreateFilesDialogUI(self)

        self.ui.folder.textChanged.connect(self.__on_path_changed)
        self.ui.basename.textChanged.connect(self.__on_path_changed)
        self.ui.header.stateChanged.connect(self.__on_file_types_changed)
        self.ui.source.stateChanged.connect(self.__on_file_types_changed)
        self.ui.create.clicked.connect(self.__on_create_clicked)
        self.ui.cancel.clicked.connect(self.__on_cancel_clicked)

    def __get_paths(self) -> Tuple[Union[str, None], Union[str, None]]:
        folder = self.ui.folder.text()
        basename = self.ui.basename.text()
        if not os.path.isdir(folder) or len(basename) == 0:
            return None, None
        return folder, basename

    def __update_create_button_status(self) -> None:
        enabled = True
        folder, basename = self.__get_paths()
        if folder is None or basename is None:
            enabled = False
        if not self.ui.header.isChecked() and not self.ui.source.isChecked():
            enabled = False
        self.ui.create.setEnabled(enabled)

    @Slot()
    def __on_path_changed(self, text: str) -> None:
        self.__update_create_button_status()

    @Slot()
    def __on_file_types_changed(self, sta) -> None:
        self.__update_create_button_status()

    @Slot()
    def __on_create_clicked(self) -> None:
        folder, basename = self.__get_paths()
        filenames: list[str] = []
        if self.ui.header.isChecked():
            path = f"{folder}\\{basename}.h"
            filenames.append(path)
            content = self.ui.header_preview.toPlainText()
            CreationUtils.create_file(path, content)
        if self.ui.source.isChecked():
            path = f"{folder}\\{basename}.cpp"
            filenames.append(path)
            content = self.ui.source_preview.toPlainText()
            CreationUtils.create_file(path, content)
        total: int = len(filenames)
        done: int = 0
        for filename in filenames:
            if os.path.isfile(filename):
                done += 1
        if total == done:
            text = f"{total} file(s) has been created"
        else:
            text = f"{total} file(s) has been created, but {total - done} failed."
        QMessageBox.information(self, "Create Files", text, QMessageBox.StandardButton.Ok)

    @Slot()
    def __on_cancel_clicked(self) -> None:
        self.reject()
