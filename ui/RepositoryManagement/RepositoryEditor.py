# coding: utf-8

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from components import DialogBase

import concepts
from bussiness import RepositoryUtils


class RepositoryEditorUI(object):

    def __init__(self, owner: QWidget):
        title_width: int = 60

        self.name_title = QLabel(text=u"Name", parent=owner)
        self.name_title.setFixedWidth(title_width)
        self.name_input = QLineEdit(parent=owner)
        self.name_layout = QHBoxLayout()
        self.name_layout.addWidget(self.name_title)
        self.name_layout.addWidget(self.name_input)

        self.path_title = QLabel(text=u"Path", parent=owner)
        self.path_title.setFixedWidth(title_width)
        self.path_input = QLineEdit(parent=owner)
        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.path_title)
        self.path_layout.addWidget(self.path_input)

        self.spacer = QSpacerItem(0, 40, vData=QSizePolicy.Policy.MinimumExpanding)

        self.left_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.ok = QPushButton(text=u"Ok", parent=owner)
        self.cancel = QPushButton(text=u"Cancel", parent=owner)
        self.right_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout = QHBoxLayout()
        self.button_layout.addSpacerItem(self.left_spacer)
        self.button_layout.addWidget(self.ok)
        self.button_layout.addWidget(self.cancel)
        self.button_layout.addSpacerItem(self.right_spacer)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.name_layout)
        self.layout.addLayout(self.path_layout)
        self.layout.addSpacerItem(self.spacer)
        self.layout.addLayout(self.button_layout)

        owner.setLayout(self.layout)


class RepositoryEditor(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None, repository_id: Optional[int] = None):
        super().__init__(parent=parent)
        self.ui = RepositoryEditorUI(owner=self)

        self.repository_id = repository_id
        if self.repository_id is None:
            self.setWindowTitle(u"Add Repository")
        else:
            self.setWindowTitle(u"Edit Repository")
            self.load_repository_info()
        self.setFixedSize(QSize(600, 300))

        self.ui.name_input.textChanged.connect(self.on_input_changed)
        self.ui.path_input.textChanged.connect(self.on_input_changed)
        self.ui.ok.clicked.connect(self.on_ok_clicked)
        self.ui.cancel.clicked.connect(self.on_cancel_clicked)

    def get_repository_info(self) -> concepts.Repository:
        return concepts.Repository(
            self.ui.name_input.text(),
            self.ui.path_input.text(),
            self.repository_id
        )

    def load_repository_info(self) -> None:
        repository = RepositoryUtils.get_repository_by_id(self.repository_id)
        if repository is not None:
            self.ui.name_input.setText(repository.name)
            self.ui.path_input.setText(repository.path)

    def on_ok_clicked(self) -> None:
        name = self.ui.name_input.text()
        path = self.ui.path_input.text()
        repo = concepts.Repository(name, path)
        if self.repository_id is None:
            RepositoryUtils.create_repository(repository=repo)
        else:
            repo.id = self.repository_id
            RepositoryUtils.update_repository(repository=repo)
        self.accept()

    def on_cancel_clicked(self) -> None:
        self.reject()

    def on_input_changed(self, text: str) -> None:
        name = self.ui.name_input.text()
        path = self.ui.path_input.text()
        enabled = len(name) != 0 and len(path) != 0
        self.ui.ok.setEnabled(enabled)
