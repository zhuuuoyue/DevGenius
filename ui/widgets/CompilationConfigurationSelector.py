# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QComboBox

from concepts import CompilationConfiguration

from ..utils import get_configuration_name


class CompilationConfigurationSelector(QComboBox):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.addItem(get_configuration_name(CompilationConfiguration.QDebug))
        self.addItem(get_configuration_name(CompilationConfiguration.Debug))
        self.addItem(get_configuration_name(CompilationConfiguration.Release))
        self.setCurrentIndex(0)

    def get_current_configuration(self, default_config: Optional[CompilationConfiguration] = None)\
            -> CompilationConfiguration:
        index = self.currentIndex()
        if 0 == index:
            return CompilationConfiguration.QDebug
        elif 1 == index:
            return CompilationConfiguration.Debug
        elif 2 == index:
            return CompilationConfiguration.Release
        return CompilationConfiguration.QDebug if default_config is None else default_config

    def set_configuration(self, config: CompilationConfiguration) -> None:
        index: int = 0
        if config == CompilationConfiguration.QDebug:
            index = 0
        elif config == CompilationConfiguration.Debug:
            index = 1
        elif config == CompilationConfiguration.Release:
            index = 2
        self.setCurrentIndex(index)


__all__ = ["CompilationConfigurationSelector"]
