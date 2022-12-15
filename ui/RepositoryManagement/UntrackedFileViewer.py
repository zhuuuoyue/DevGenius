# coding: utf-8

from typing import Optional, Union

from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QListWidget

from components import WidgetBase
from bussiness import RepositoryUtils


class UntrackedFileList(QListWidget):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

    def set_untracked_files(self, files: list[str]) -> None:
        while self.count():
            self.takeItem(0)
        self.addItems(files)


class UntrackedFileViewerUI(object):

    def __init__(self, owner: QWidget):
        self.list = UntrackedFileList(parent=owner)

        self.list_layout = QHBoxLayout()
        self.list_layout.addWidget(self.list)

        self.group_box = QGroupBox(parent=owner)
        self.group_box.setTitle(u"Untracked Files")
        self.group_box.setLayout(self.list_layout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.group_box)

        owner.setLayout(self.layout)


class UntrackedFileViewer(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__ui = UntrackedFileViewerUI(self)

    def set_repository_directory(self, directory: Union[str, None]) -> None:
        files: list[str] = [] if directory is None else RepositoryUtils.get_untracked_files(directory=directory)
        self.__ui.list.set_untracked_files(files)


__all__ = ["UntrackedFileViewer"]
