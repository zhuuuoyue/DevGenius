# coding: utf-8

from typing import Optional, Any

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QDialog, QMessageBox

import concepts
from concepts import Repository
from bussiness import get_repositories
from components import EditableList, ListItemFormatter, ListItemFilter

from .RepositoryEditor import RepositoryEditor
from bussiness import RepositoryUtils


class RepositoryFormatter(ListItemFormatter):

    def format(self, item: Repository, items: list[Any] = None, index: Optional[int] = None) -> str:
        if not isinstance(item, Repository):
            return "<error item>"
        if len(item.path) == 0:
            return "<invalid repository>"
        if len(item.name) == 0:
            return item.path
        return f"{item.name}[ {item.path} ]"


class RepositoryFilter(ListItemFilter):

    def filter(self, item: Any, keyword: str, items: list[Any] = None, index: Optional[int] = None) -> bool:
        if not isinstance(item, Repository):
            return False
        lower_path = item.path.lower()
        lower_keyword = keyword.lower()
        return lower_keyword in lower_path


class RepositoryList(EditableList):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, item_formatter=RepositoryFormatter(), item_filter=RepositoryFilter(),
                         *args, **kwargs)
        self.setFixedWidth(240)
        self._repositories = get_repositories()
        self.load_data(self._repositories)

        self.add_clicked.connect(self.on_add_clicked)
        self.delete_clicked.connect(self.on_delete_clicked)
        self.edit_clicked.connect(self.on_edit_clicked)

    @Slot()
    def on_add_clicked(self) -> None:
        dialog = RepositoryEditor(self)
        if QDialog.DialogCode.Accepted == dialog.exec():
            self.refresh_data()

    @Slot()
    def on_delete_clicked(self) -> None:
        repos = self.get_selected_items()
        if len(repos) != 1:
            return
        repo: concepts.Repository = repos[0]
        result = QMessageBox.warning(
            self,
            u"Delete Repository",
            f"The repository will be deleted.\nname: {repo.name}\npath: {repo.path}",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Cancel
        )
        if result == QMessageBox.StandardButton.Ok:
            RepositoryUtils.delete_repository(repo.id)
            self.refresh_data()

    @Slot()
    def on_edit_clicked(self) -> None:
        repos = self.get_selected_items()
        if len(repos) != 1:
            return
        repo: concepts.Repository = repos[0]
        dialog = RepositoryEditor(self, repo.id)
        if QDialog.DialogCode.Accepted == dialog.exec():
            repo = dialog.get_repository_info()
            RepositoryUtils.update_repository(repo)
            self.refresh_data()

    def refresh_data(self) -> None:
        repos: list[concepts.Repository] = RepositoryUtils.get_repositories()
        self.load_data(repos)


__all__ = ["RepositoryList"]
