# coding: utf-8

from typing import Optional, Any

from PySide6.QtWidgets import QWidget

from concepts import Repository
from bussiness import get_repositories
from zui import EditableList, ListItemFormatter, ListItemFilter


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


class ProjectList(EditableList):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, item_formatter=RepositoryFormatter(), item_filter=RepositoryFilter(),
                         *args, **kwargs)
        self.setFixedWidth(240)
        self._repositories = get_repositories()
        self.load_data(self._repositories)


__all__ = ["ProjectList"]
