# coding: utf-8

from typing import Optional

from PySide6.QtCore import Slot, QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

import concepts
from components import DialogBase

from .RepositoryList import RepositoryList
from .RepositoryInfoViewer import RepositoryInfoViewer
from .BranchInfoViewer import BranchInfoViewer
from .UntrackedFileViewer import UntrackedFileViewer


class RepositoryManagementDialogUI(object):

    def __init__(self, owner: QWidget):
        self.layout = QHBoxLayout()

        self.project_list = RepositoryList(owner)
        self.layout.addWidget(self.project_list)

        self.right_layout = QVBoxLayout()

        self.repository_viewer = RepositoryInfoViewer(owner)
        self.right_layout.addWidget(self.repository_viewer)

        self.branch_viewer = BranchInfoViewer(owner)
        self.right_layout.addWidget(self.branch_viewer)

        self.untracked_file_viewer = UntrackedFileViewer(owner)
        self.right_layout.addWidget(self.untracked_file_viewer)

        self.spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.right_layout.addSpacerItem(self.spacer)

        self.layout.addLayout(self.right_layout)
        owner.setLayout(self.layout)


class RepositoryManagementDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, dialog_id="93aa2d30-6410-40b9-88b3-37d53f9e0d1a", *args, **kwargs)
        self.setWindowTitle(u"Repository Management")
        self.setMinimumSize(QSize(800, 600))
        self.ui = RepositoryManagementDialogUI(self)

        self.ui.project_list.selection_changed.connect(self._on_repository_changed)

    @Slot()
    def _on_repository_changed(self):
        repos = self.ui.project_list.get_selected_items()
        if len(repos) != 0:
            repo: concepts.Repository = repos[0]
            self.ui.repository_viewer.set_repository(repo)
            self.ui.branch_viewer.set_repository_directory(repo.path)
            self.ui.untracked_file_viewer.set_repository_directory(repo.path)
        else:
            self.ui.repository_viewer.set_repository(None)
            self.ui.branch_viewer.set_repository_directory(None)
            self.ui.untracked_file_viewer.set_repository_directory(None)


__all__ = ["RepositoryManagementDialog"]
