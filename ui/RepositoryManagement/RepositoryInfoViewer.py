# coding: utf-8

from typing import Optional, Union

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QGroupBox

from concepts import Repository
from bussiness import RepositoryUtils
from components import PathLabel, DirectoryPathValidator, FilePathValidator
from components.WidgetBase import WidgetBase

from .OutputDirectoryBar import OutputDirectoryBar
from .SolutionDirectoryBar import SolutionDirectoryBar
from .CodeReviewBar import CodeReviewBar


class RepositoryInfoViewerUI(object):

    def __init__(self, owner: QWidget, title_width: Optional[int] = None):
        if title_width is None:
            title_width = 120

        self.file_validator = FilePathValidator()
        self.directory_validator = DirectoryPathValidator()

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
        self.path_input = PathLabel(parent=owner, validator=self.directory_validator)
        self.path_input.setDisabled(True)
        self.path_layout.addWidget(self.path_input)

        self.solution_layout = QHBoxLayout()
        self.solution_title = QLabel(text=u"Solution Directory", parent=owner)
        self.solution_title.setFixedWidth(title_width)
        self.solution_layout.addWidget(self.solution_title)
        self.solution_input = SolutionDirectoryBar(parent=owner)
        self.solution_layout.addWidget(self.solution_input)

        self.debug_layout = QHBoxLayout()
        self.debug_title = QLabel(text=u"Debug Output Dir.", parent=owner)
        self.debug_title.setFixedWidth(title_width)
        self.debug_layout.addWidget(self.debug_title)
        self.debug_input = OutputDirectoryBar(parent=owner)
        self.debug_layout.addWidget(self.debug_input)

        self.q_debug_layout = QHBoxLayout()
        self.q_debug_title = QLabel(text=u"QDebug Output Dir.", parent=owner)
        self.q_debug_title.setFixedWidth(title_width)
        self.q_debug_layout.addWidget(self.q_debug_title)
        self.q_debug_input = OutputDirectoryBar(parent=owner)
        self.q_debug_layout.addWidget(self.q_debug_input)

        self.release_layout = QHBoxLayout()
        self.release_title = QLabel(text=u"Release Output Dir.", parent=owner)
        self.release_title.setFixedWidth(title_width)
        self.release_layout.addWidget(self.release_title)
        self.release_input = OutputDirectoryBar(parent=owner)
        self.release_layout.addWidget(self.release_input)

        self.code_review_layout = QHBoxLayout()
        self.code_review_title = QLabel(text=u"Code_Review.bat", parent=owner)
        self.code_review_title.setFixedWidth(title_width)
        self.code_review_layout.addWidget(self.code_review_title)
        self.code_review_input = CodeReviewBar(parent=owner)
        self.code_review_layout.addWidget(self.code_review_input)

        self.inner_layout = QVBoxLayout()
        self.inner_layout.addLayout(self.name_layout)
        self.inner_layout.addLayout(self.path_layout)
        self.inner_layout.addLayout(self.solution_layout)
        self.inner_layout.addLayout(self.debug_layout)
        self.inner_layout.addLayout(self.q_debug_layout)
        self.inner_layout.addLayout(self.release_layout)
        self.inner_layout.addLayout(self.code_review_layout)

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
            self.ui.path_input.set_path(repo.path)
            self.ui.solution_input.set_path(dirs["solution"])
            self.ui.debug_input.set_path(dirs["debug"])
            self.ui.release_input.set_path(dirs["release"])
            self.ui.q_debug_input.set_path(dirs["q_debug"])
            self.ui.code_review_input.set_path(dirs["code_review"])
        else:
            self.clear()

    def clear(self) -> None:
        self.ui.name_input.setText(u"")
        self.ui.path_input.set_path(None)
        self.ui.solution_input.set_path(None)
        self.ui.debug_input.set_path(None)
        self.ui.release_input.set_path(None)
        self.ui.q_debug_input.set_path(None)
        self.ui.code_review_input.set_path(None)


__all__ = ["RepositoryInfoViewer"]
