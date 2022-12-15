# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLineEdit

from concepts.test import TestCase
from components import Form, FormRowInfo


def create_label(parent: QWidget) -> QLineEdit:
    label = QLineEdit(parent=parent)
    return label


class TestCaseInfoPanelUI(object):

    def __init__(self, owner: QWidget):
        self.group = create_label(owner)
        self.name = create_label(owner)
        self.run_time_limited = create_label(owner)
        self.run_speed = create_label(owner)
        self.count = create_label(owner)
        self.debug_mode = create_label(owner)
        self.js_filename = create_label(owner)
        self.to_run = create_label(owner)
        self.run_type = create_label(owner)
        self.exe_name = create_label(owner)
        self.depend_on_source = create_label(owner)
        self.directory = create_label(owner)
        rows = [
            FormRowInfo(title=u"输出目录", value=self.group),
            FormRowInfo(title=u"输出目录", value=self.name),
            FormRowInfo(title=u"输出目录", value=self.run_time_limited),
            FormRowInfo(title=u"输出目录", value=self.run_speed),
            FormRowInfo(title=u"输出目录", value=self.count),
            FormRowInfo(title=u"输出目录", value=self.debug_mode),
            FormRowInfo(title=u"输出目录", value=self.js_filename),
            FormRowInfo(title=u"输出目录", value=self.to_run),
            FormRowInfo(title=u"输出目录", value=self.run_type),
            FormRowInfo(title=u"输出目录", value=self.exe_name),
            FormRowInfo(title=u"输出目录", value=self.depend_on_source),
            FormRowInfo(title=u"输出目录", value=self.directory),
        ]
        self.central_widget = Form(rows, owner)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central_widget)
        owner.setLayout(self.layout)


class TestCaseInfoPanel(QGroupBox):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent=parent)
        self.setTitle(u"测试用例信息")
        self.__ui = TestCaseInfoPanelUI(self)

    def remove_data(self) -> None:
        pass

    def set_data(self, data: Optional[TestCase]) -> None:
        if isinstance(data, TestCase):
            self.__ui.group.setText("" if data.group is None else data.group)
        else:
            self.remove_data()

