# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QRadioButton, QLineEdit, QGroupBox, QHBoxLayout, QVBoxLayout, QSpacerItem,\
    QSizePolicy

from components import WidgetBase

from ..widgets import OutputDirectorySelector


class ProgramDirectorySelectorUI(object):

    def __init__(self, owner: QWidget):
        indent = 20

        self.use_repository_output = QRadioButton(text=u"Use solution output directory", parent=owner)

        self.output_directory_selector_indent = QSpacerItem(indent, 0, hData=QSizePolicy.Policy.Fixed)
        self.output_directory_selector = OutputDirectorySelector(parent=owner)
        self.output_directory_selector_layout = QHBoxLayout()
        self.output_directory_selector_layout.addSpacerItem(self.output_directory_selector_indent)
        self.output_directory_selector_layout.addWidget(self.output_directory_selector)

        self.output_directory_input_indent = QSpacerItem(indent, 0, hData=QSizePolicy.Policy.Fixed)
        self.output_directory_input = QLineEdit(parent=owner)
        self.output_directory_input_layout = QHBoxLayout()
        self.output_directory_input_layout.addSpacerItem(self.output_directory_input_indent)
        self.output_directory_input_layout.addWidget(self.output_directory_input)

        self.use_custom_software_package = QRadioButton(text=u"Use custom program directory", parent=owner)

        self.program_directory_input_indent = QSpacerItem(indent, 0, hData=QSizePolicy.Policy.Fixed)
        self.program_directory_input = QLineEdit(parent=owner)
        self.program_directory_input_layout = QHBoxLayout()
        self.program_directory_input_layout.addSpacerItem(self.program_directory_input_indent)
        self.program_directory_input_layout.addWidget(self.program_directory_input)

        self.inner_layout = QVBoxLayout()
        self.inner_layout.addWidget(self.use_repository_output)
        self.inner_layout.addLayout(self.output_directory_selector_layout)
        self.inner_layout.addLayout(self.output_directory_input_layout)
        self.inner_layout.addWidget(self.use_custom_software_package)
        self.inner_layout.addLayout(self.program_directory_input_layout)

        self.group = QGroupBox(title=u"Select program directory", parent=owner)
        self.group.setLayout(self.inner_layout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.group)

        owner.setLayout(self.layout)


class ProgramDirectorySelector(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.ui = ProgramDirectorySelectorUI(self)
    #     self.output_directory_selector.value_changed.connect(self._on_output_directory_changed)
    #
    # @Slot(str)
    # def _on_output_directory_changed(self, path: str):
    #     self.output_directory_input.setText(path)
