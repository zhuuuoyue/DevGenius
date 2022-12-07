# coding: utf-8

from typing import Optional, Union

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QGroupBox

from concepts import Repository
from bussiness import RepositoryUtils
from components.WidgetBase import WidgetBase


class RepositoryInfoViewerUI(object):

    def __init__(self, owner: QWidget, title_width: Optional[int] = None):
        if title_width is None:
            title_width = 120

        self.name_layout = QHBoxLayout()
        self.name_title = QLabel(text=u"Name", parent=owner)
        self.name_title.setFixedWidth(title_width)
        self.name_layout.addWidget(self.name_title)
        self.name_input = QLineEdit(parent=owner)
        self.name_input.setDisabled(True)
        self.name_layout.addWidget(self.name_input)

        self.path_layout = QHBoxLayout()
        self.path_title = QLabel(text=u"Root Path", parent=owner)
        self.path_title.setFixedWidth(title_width)
        self.path_layout.addWidget(self.path_title)
        self.path_input = QLineEdit(parent=owner)
        self.path_input.setDisabled(True)
        self.path_layout.addWidget(self.path_input)

        self.solution_layout = QHBoxLayout()
        self.solution_title = QLabel(text=u"Solution Directory", parent=owner)
        self.solution_title.setFixedWidth(title_width)
        self.solution_layout.addWidget(self.solution_title)
        self.solution_input = QLineEdit(parent=owner)
        self.solution_input.setDisabled(True)
        self.solution_layout.addWidget(self.solution_input)

        self.debug_layout = QHBoxLayout()
        self.debug_title = QLabel(text=u"Debug Output Dir.", parent=owner)
        self.debug_title.setFixedWidth(title_width)
        self.debug_layout.addWidget(self.debug_title)
        self.debug_input = QLineEdit(parent=owner)
        self.debug_input.setDisabled(True)
        self.debug_layout.addWidget(self.debug_input)

        self.qdebug_layout = QHBoxLayout()
        self.qdebug_title = QLabel(text=u"QDebug Output Dir.", parent=owner)
        self.qdebug_title.setFixedWidth(title_width)
        self.qdebug_layout.addWidget(self.qdebug_title)
        self.qdebug_input = QLineEdit(parent=owner)
        self.qdebug_input.setDisabled(True)
        self.qdebug_layout.addWidget(self.qdebug_input)

        self.release_layout = QHBoxLayout()
        self.release_title = QLabel(text=u"Release Output Dir.", parent=owner)
        self.release_title.setFixedWidth(title_width)
        self.release_layout.addWidget(self.release_title)
        self.release_input = QLineEdit(parent=owner)
        self.release_input.setDisabled(True)
        self.release_layout.addWidget(self.release_input)

        self.inner_layout = QVBoxLayout()
        self.inner_layout.addLayout(self.name_layout)
        self.inner_layout.addLayout(self.path_layout)
        self.inner_layout.addLayout(self.solution_layout)
        self.inner_layout.addLayout(self.debug_layout)
        self.inner_layout.addLayout(self.qdebug_layout)
        self.inner_layout.addLayout(self.release_layout)

        self.group_box = QGroupBox(parent=owner)
        self.group_box.setTitle(u"Project Basic Information")
        self.group_box.setLayout(self.inner_layout)

        self.outer_layout = QHBoxLayout()
        self.outer_layout.addWidget(self.group_box)

        owner.setLayout(self.outer_layout)


class RepositoryInfoViewer(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.ui = RepositoryInfoViewerUI(owner=self)

    def set_repository(self, repo: Union[Repository, None]) -> None:
        if isinstance(repo, Repository):
            dirs = RepositoryUtils.get_repository_directories(repo)
            self.ui.name_input.setText(repo.name)
            self.ui.path_input.setText(repo.path)
            self.ui.solution_input.setText(dirs["solution"])
            self.ui.debug_input.setText(dirs["debug"])
            self.ui.release_input.setText(dirs["release"])
            self.ui.qdebug_input.setText(dirs["qdebug"])
        else:
            self.clear()

    def clear(self) -> None:
        self.ui.name_input.setText(u"")
        self.ui.path_input.setText(u"")
        self.ui.solution_input.setText(u"")
        self.ui.debug_input.setText(u"")
        self.ui.release_input.setText(u"")
        self.ui.qdebug_input.setText(u"")


__all__ = ["RepositoryInfoViewer"]
