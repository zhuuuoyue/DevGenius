# coding: utf-8

from typing import Optional

from PySide6.QtCore import Slot, QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from zui import DialogBase

from .ProjectList import ProjectList
from .ProjectInfoViewer import ProjectInfoViewer
from .RepositoryInfoViewer import RepositoryInfoViewer


class ProjectManagementDialogUI(object):

    def __init__(self, owner: QWidget):
        self.layout = QHBoxLayout()

        self.project_list = ProjectList(owner)
        self.layout.addWidget(self.project_list)

        self.right_layout = QVBoxLayout()
        self.project_info_viewer = ProjectInfoViewer(owner)
        self.right_layout.addWidget(self.project_info_viewer)
        self.repository_info_viewer = RepositoryInfoViewer(owner)
        self.right_layout.addWidget(self.repository_info_viewer)
        self.spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.right_layout.addSpacerItem(self.spacer)
        self.layout.addLayout(self.right_layout)

        owner.setLayout(self.layout)


class ProjectManagementDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle(u"Project Management")
        self.setMinimumSize(QSize(800, 600))
        self.ui = ProjectManagementDialogUI(self)

        self.ui.project_list.selection_changed.connect(self._on_repository_changed)

    @Slot()
    def _on_repository_changed(self):
        repos = self.ui.project_list.get_selected_items()
        if len(repos) != 0:
            self.ui.project_info_viewer.set_repository(repos[0])


__all__ = ["ProjectManagementDialog"]
