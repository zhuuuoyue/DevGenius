# coding: utf-8

import os
from typing import Optional, Tuple, Union

from PySide6.QtCore import QSize, Slot
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QCheckBox, QLabel, QSpacerItem,
                               QSizePolicy, QTabWidget, QTextEdit, QPushButton, QMessageBox)

from utils import save_file_as_utf8_bom
from bussiness.creation import get_header_content, get_source_content
from components import DialogBase


def create_title(title: str, parent: Optional[QWidget] = None) -> QLabel:
    widget = QLabel(text=title, parent=parent)
    widget.setFixedWidth(80)
    return widget


class Setting(object):

    def __init__(self):
        self.directory = None
        self.header = True
        self.source = True


class CreateFilesDialogUI(object):

    def __init__(self, owner: QWidget):
        self.folder_layout = QHBoxLayout()
        self.folder_title = create_title(u"目标文件夹", parent=owner)
        self.folder_layout.addWidget(self.folder_title)
        self.folder = QLineEdit(parent=owner)
        self.folder_layout.addWidget(self.folder)

        self.basename_layout = QHBoxLayout()
        self.basename_title = create_title(u"文件名", parent=owner)
        self.basename_layout.addWidget(self.basename_title)
        self.basename = QLineEdit(parent=owner)
        self.basename_layout.addWidget(self.basename)

        self.extension_layout = QHBoxLayout()
        self.extension_title = create_title(u"文件类型", parent=owner)
        self.extension_layout.addWidget(self.extension_title)
        self.header = QCheckBox(text=u"头文件 (*.h)", parent=owner)
        self.extension_layout.addWidget(self.header)
        self.source = QCheckBox(text=u"源文件 (*.cpp)", parent=owner)
        self.extension_layout.addWidget(self.source)
        self.extension_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.extension_layout.addSpacerItem(self.extension_spacer)

        self.preview = QTabWidget(parent=owner)
        self.header_preview = CreateFilesDialogUI.create_text_editor(parent=owner, content=get_header_content())
        self.preview.addTab(self.header_preview, u"头文件")
        self.source_preview = CreateFilesDialogUI.create_text_editor(parent=owner, content=get_source_content())
        self.preview.addTab(self.source_preview, u"源文件")

        self.button_layout = QHBoxLayout()
        self.spacer_before_create = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout.addSpacerItem(self.spacer_before_create)
        self.create = QPushButton(text=u"创建", parent=owner)
        self.create.setEnabled(False)
        self.button_layout.addWidget(self.create)
        self.cancel = QPushButton(text=u"取消", parent=owner)
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

    @staticmethod
    def create_text_editor(parent: QWidget, content: str) -> QTextEdit:
        editor: QTextEdit = QTextEdit(parent=parent)
        editor.setText(content)
        editor.setStyleSheet("""
        font-family: Consolas;
        """)
        return editor


class CreateFilesDialog(DialogBase):
    __cache: Setting = Setting()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="46d861c9-a8b7-440f-8a3f-929288551787")
        self.setWindowTitle(u"创建文件")
        self.setMinimumSize(QSize(600, 400))
        self.ui = CreateFilesDialogUI(self)

        self.__load_data(CreateFilesDialog.__cache)

        self.ui.folder.textChanged.connect(self.__on_path_changed)
        self.ui.basename.textChanged.connect(self.__on_basename_changed)
        self.ui.header.stateChanged.connect(self.__on_file_types_changed)
        self.ui.source.stateChanged.connect(self.__on_file_types_changed)
        self.ui.create.clicked.connect(self.__on_create_clicked)
        self.ui.cancel.clicked.connect(self.__on_cancel_clicked)

        self.__update_create_button_status()

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
    def __on_basename_changed(self) -> None:
        header_basename = self.ui.basename.text()
        if 0 == len(header_basename):
            source = get_source_content()
        else:
            source = get_source_content(header_filename=f"{header_basename}.h")
        self.ui.source_preview.setPlainText(source)
        self.__update_create_button_status()

    @Slot()
    def __on_path_changed(self) -> None:
        self.__save_data()
        self.__update_create_button_status()

    @Slot()
    def __on_file_types_changed(self) -> None:
        self.__save_data()
        self.__update_create_button_status()

    @Slot()
    def __on_create_clicked(self) -> None:
        folder, basename = self.__get_paths()
        filenames: list[str] = []
        if self.ui.header.isChecked():
            path = os.path.join(folder, f"{basename}.h")
            filenames.append(path)
            content = self.ui.header_preview.toPlainText()
            save_file_as_utf8_bom(path, content)
        if self.ui.source.isChecked():
            path = os.path.join(folder, f"{basename}.cpp")
            filenames.append(path)
            content = self.ui.source_preview.toPlainText()
            save_file_as_utf8_bom(path, content)
        total: int = len(filenames)
        done: int = 0
        for filename in filenames:
            if os.path.isfile(filename):
                done += 1
        if total == done:
            text = f"已创建 {total} 个文件"
        else:
            text = f"希望创建 {total} 个文件，但只创建了 {done} 个文件，有 {total - done} 个文件创建失败"
        QMessageBox.information(self, "创建文件完成", text, QMessageBox.StandardButton.Ok)

    @Slot()
    def __on_cancel_clicked(self) -> None:
        self.reject()

    def __load_data(self, data: Setting) -> None:
        self.ui.folder.setText(data.directory)
        self.ui.header.setChecked(data.header)
        self.ui.source.setChecked(data.source)

    def __save_data(self) -> None:
        CreateFilesDialog.__cache.directory = self.ui.folder.text()
        CreateFilesDialog.__cache.header = self.ui.header.isChecked()
        CreateFilesDialog.__cache.source = self.ui.source.isChecked()
