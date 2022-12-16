# coding: utf-8

from typing import Optional

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtWidgets import QWidget, QTabWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from components import DialogBase

from .ISettingEditor import ISettingEditor
from .CreateFileSettingsEditor import CreateFileSettingsEditor


class PreferenceDialogUI(object):

    def __init__(self, owner: QWidget):
        self.tab_widget = QTabWidget(parent=owner)
        self.tabs: list[ISettingEditor] = []

        self.tab_create_file = CreateFileSettingsEditor(parent=owner)
        self.tab_widget.addTab(self.tab_create_file, u"创建文件")
        self.tabs.append(self.tab_create_file)

        self.bottom_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.apply_button = QPushButton(u"应用", parent=owner)
        self.apply_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.ok_button = QPushButton(u"确定", parent=owner)
        self.ok_button.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.cancel_button = QPushButton(u"取消", parent=owner)
        self.cancel_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(8)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.addSpacerItem(self.bottom_spacer)
        self.bottom_layout.addWidget(self.apply_button)
        self.bottom_layout.addWidget(self.ok_button)
        self.bottom_layout.addWidget(self.cancel_button)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.addWidget(self.tab_widget)
        self.layout.addLayout(self.bottom_layout)

        owner.setWindowTitle(u"设置")
        owner.setFixedSize(QSize(600, 400))
        owner.setLayout(self.layout)


class PreferencesDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent, dialog_id="83e4862a-504c-481d-8a56-ba976863236e")
        self.__ui = PreferenceDialogUI(self)

        self.__ui.apply_button.clicked.connect(self.__on_apply_clicked)
        self.__ui.ok_button.clicked.connect(self.__on_ok_clicked)
        self.__ui.cancel_button.clicked.connect(self.__on_exit_clicked)

    def __save(self) -> None:
        for page in self.__ui.tabs:
            page.apply_modification()

    @Slot()
    def __on_apply_clicked(self) -> None:
        self.__save()

    @Slot()
    def __on_ok_clicked(self) -> None:
        self.__save()
        self.accept()

    @Slot()
    def __on_exit_clicked(self) -> None:
        self.reject()
