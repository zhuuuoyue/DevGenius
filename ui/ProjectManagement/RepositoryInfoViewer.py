# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget

from zui import WidgetBase


class RepositoryInfoViewer(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)


__all__ = ["RepositoryInfoViewer"]
