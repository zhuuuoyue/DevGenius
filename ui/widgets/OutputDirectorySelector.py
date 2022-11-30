# coding: utf-8

from typing import Optional

from PySide6.QtCore import QMargins, Slot, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout

from zui import WidgetBase

from ..utils import get_configuration_name
from .ProjectSelector import ProjectSelector
from .CompilationConfigurationSelector import CompilationConfigurationSelector


class OutputDirectorySelector(WidgetBase):

    value_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.project_selector = ProjectSelector(parent=self)
        self.configuration_selector = CompilationConfigurationSelector(parent=self)
        self.configuration_selector.setMaximumWidth(80)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.layout.addWidget(self.project_selector)
        self.layout.addWidget(self.configuration_selector)
        self.setLayout(self.layout)

        self.project_selector.currentIndexChanged.connect(self._on_current_index_changed)
        self.configuration_selector.currentIndexChanged.connect(self._on_current_index_changed)

    def get_output_directory(self) -> str:
        repository = self.project_selector.get_current_project()
        config = self.configuration_selector.get_current_configuration()
        return f"{repository.path}\\bin\\{get_configuration_name(config)}"

    @Slot()
    def _on_current_index_changed(self):
        self.value_changed.emit(self.get_output_directory())


__all__ = ["OutputDirectorySelector"]
