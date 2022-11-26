# coding: utf-8

from typing import Optional, Any

from PySide6.QtCore import Slot, Signal, QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QGroupBox, QLabel, QLineEdit

from .command import ICommand
from .WindowManager import get_window_manager
from .widgets import DialogBase, AdvList, WidgetBase
from .widgets.AdvList import (AdvListItemFormatter, AdvListItemFilter)

from concepts import Repository
from op import get_repositories


class RepositoryFormatter(AdvListItemFormatter):

    def format(self, item: Repository, items: list[Any] = None, index: Optional[int] = None) -> str:
        if not isinstance(item, Repository):
            return "<error item>"
        if len(item.path) == 0:
            return "<invalid repository>"
        if len(item.name) == 0:
            return item.path
        return f"{item.name}[ {item.path} ]"


class RepositoryFilter(AdvListItemFilter):

    def filter(self, item: Any, keyword: str, items: list[Any] = None, index: Optional[int] = None) -> bool:
        if not isinstance(item, Repository):
            return False
        lower_path = item.path.lower()
        lower_keyword = keyword.lower()
        return lower_keyword in lower_path


class ProjectList(AdvList):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(
            parent=parent,
            formatter=RepositoryFormatter(),
            filter=RepositoryFilter(),
            *args,
            **kwargs
        )
        self.setFixedWidth(240)

        self._repositories = get_repositories()
        self.load_data(self._repositories)


class ProjectInfoViewer(QWidget):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        title_width = 60

        self.name_layout = QHBoxLayout()
        self.name_title = QLabel(text=u"名称", parent=self)
        self.name_title.setFixedWidth(title_width)
        self.name_layout.addWidget(self.name_title)
        self.name_input = QLineEdit(parent=self)
        self.name_input.setDisabled(True)
        self.name_layout.addWidget(self.name_input)

        self.path_layout = QHBoxLayout()
        self.path_title = QLabel(text=u"路径", parent=self)
        self.path_title.setFixedWidth(title_width)
        self.path_layout.addWidget(self.path_title)
        self.path_input = QLineEdit(parent=self)
        self.path_input.setDisabled(True)
        self.path_layout.addWidget(self.path_input)

        self.debug_layout = QHBoxLayout()
        self.debug_title = QLabel(text=u"Debug", parent=self)
        self.debug_title.setFixedWidth(title_width)
        self.debug_layout.addWidget(self.debug_title)
        self.debug_input = QLineEdit(parent=self)
        self.debug_input.setDisabled(True)
        self.debug_layout.addWidget(self.debug_input)

        self.qdebug_layout = QHBoxLayout()
        self.qdebug_title = QLabel(text=u"QDebug", parent=self)
        self.qdebug_title.setFixedWidth(title_width)
        self.qdebug_layout.addWidget(self.qdebug_title)
        self.qdebug_input = QLineEdit(parent=self)
        self.qdebug_input.setDisabled(True)
        self.qdebug_layout.addWidget(self.qdebug_input)

        self.release_layout = QHBoxLayout()
        self.release_title = QLabel(text=u"Release", parent=self)
        self.release_title.setFixedWidth(title_width)
        self.release_layout.addWidget(self.release_title)
        self.release_input = QLineEdit(parent=self)
        self.release_input.setDisabled(True)
        self.release_layout.addWidget(self.release_input)

        self.inner_layout = QVBoxLayout()
        self.inner_layout.addLayout(self.name_layout)
        self.inner_layout.addLayout(self.path_layout)
        self.inner_layout.addLayout(self.debug_layout)
        self.inner_layout.addLayout(self.qdebug_layout)
        self.inner_layout.addLayout(self.release_layout)

        self.group_box = QGroupBox(parent=self)
        self.group_box.setTitle(u"项目信息")
        self.group_box.setLayout(self.inner_layout)

        self.outer_layout = QHBoxLayout()
        self.outer_layout.addWidget(self.group_box)

        self.setLayout(self.outer_layout)

    def set_repository(self, repo: Repository) -> None:
        if isinstance(repo, Repository):
            self.name_input.setText(repo.name)
            self.path_input.setText(repo.path)
        else:
            self.name_input.setText(u"")
            self.path_input.setText(u"")


class RepositoryInfoViewer(QWidget):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)


class ProjectDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle(u"项目管理")
        self.setFixedSize(QSize(800, 600))

        self.layout = QHBoxLayout()

        self.list = ProjectList(self)
        self.layout.addWidget(self.list)

        self.right_layout = QVBoxLayout()
        self.project_info_viewer = ProjectInfoViewer(self)
        self.right_layout.addWidget(self.project_info_viewer)
        self.repository_info_viewer = RepositoryInfoViewer(self)
        self.right_layout.addWidget(self.repository_info_viewer)
        self.spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.right_layout.addSpacerItem(self.spacer)
        self.layout.addLayout(self.right_layout)

        self.setLayout(self.layout)

        self.list.selection_changed.connect(self._on_repository_changed)

    @Slot()
    def _on_repository_changed(self):
        repo = self.list.get_selected_project()
        self.project_info_viewer.set_repository(repo)


class ProjectCommand(ICommand):

    def __init__(self):
        super().__init__()

    def execute(self, *args, **kwargs) -> None:
        dialog = ProjectDialog(get_window_manager().get_main_window())
        dialog.exec()

