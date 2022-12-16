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
            FormRowInfo(title=u"用例名称", value=self.name),
            FormRowInfo(title=u"运行时限", value=self.run_time_limited),
            FormRowInfo(title=u"运行速度", value=self.run_speed),
            FormRowInfo(title=u"数量", value=self.count),
            FormRowInfo(title=u"调试模式", value=self.debug_mode),
            FormRowInfo(title=u"脚本文件名", value=self.js_filename),
            FormRowInfo(title=u"是否执行", value=self.to_run),
            FormRowInfo(title=u"运行类型", value=self.run_type),
            FormRowInfo(title=u"可执行文件", value=self.exe_name),
            FormRowInfo(title=u"依赖于源码", value=self.depend_on_source),
            FormRowInfo(title=u"测试用例目录", value=self.directory),
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
        self.__ui.group.setText("")
        self.__ui.name.setText("")
        self.__ui.run_time_limited.setText("")
        self.__ui.run_speed.setText("")
        self.__ui.count.setText("")
        self.__ui.debug_mode.setText("")
        self.__ui.js_filename.setText("")
        self.__ui.to_run.setText("")
        self.__ui.run_type.setText("")
        self.__ui.exe_name.setText("")
        self.__ui.depend_on_source.setText("")
        self.__ui.directory.setText("")

    def set_data(self, data: Optional[TestCase]) -> None:
        if isinstance(data, TestCase):
            unset: str = ""
            self.__ui.group.setText(unset if data.group is None else data.group)
            self.__ui.name.setText(unset if data.name is None else data.name)
            self.__ui.run_time_limited.setText(unset if data.run_time_limited is None else f"{data.run_time_limited} s")
            self.__ui.run_speed.setText(unset if data.run_speed is None else f"{data.run_speed} ms")
            self.__ui.count.setText(unset if data.count is None else str(data.count))
            self.__ui.debug_mode.setText(unset if data.debug_mode is None else data.debug_mode)
            self.__ui.js_filename.setText(unset if data.js_filename is None else data.js_filename)
            self.__ui.to_run.setText(unset if data.to_run is None else str(data.to_run))
            self.__ui.run_type.setText(unset if data.run_type is None else data.run_type)
            self.__ui.exe_name.setText(unset if data.exe_name is None else data.exe_name)
            self.__ui.depend_on_source.setText(unset if data.depend_on_source is None else str(data.depend_on_source))
            self.__ui.directory.setText(unset if data.directory is None else data.directory)
        else:
            self.remove_data()

