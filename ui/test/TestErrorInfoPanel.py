# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLineEdit

from concepts.test import TestCaseRunningError
from components import Form, FormRowInfo


def create_label(parent: QWidget) -> QLineEdit:
    label = QLineEdit(parent=parent)
    return label


class TestErrorInfoPanelUI(object):

    def __init__(self, owner: QWidget):
        self.name = create_label(owner)
        self.task_id = create_label(owner)
        self.filename = create_label(owner)
        self.line_number = create_label(owner)
        self.function = create_label(owner)
        self.message = create_label(owner)
        self.author = create_label(owner)
        self.date = create_label(owner)
        rows = [
            FormRowInfo(title=u"错误名称", value=self.name),
            FormRowInfo(title=u"任务 ID", value=self.task_id),
            FormRowInfo(title=u"文件名", value=self.filename),
            FormRowInfo(title=u"行号", value=self.line_number),
            FormRowInfo(title=u"函数/方法", value=self.function),
            FormRowInfo(title=u"调试信息", value=self.message),
            FormRowInfo(title=u"作者", value=self.author),
            FormRowInfo(title=u"日期", value=self.date),
        ]
        self.central_widget = Form(rows, owner)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central_widget)
        owner.setLayout(self.layout)


class TestErrorInfoPanel(QGroupBox):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent=parent)
        self.setTitle(u"错误信息")
        self.__ui = TestErrorInfoPanelUI(self)

    def set_data(self, data: Optional[TestCaseRunningError]) -> None:
        if isinstance(data, TestCaseRunningError):
            if data.name is not None:
                self.__ui.name.setText(data.name)
        else:
            self.clean()

    def clean(self) -> None:
        self.__ui.name.setText(u"")
        self.__ui.task_id.setText(u"")
        self.__ui.filename.setText(u"")
        self.__ui.line_number.setText(u"")
        self.__ui.function.setText(u"")
        self.__ui.message.setText(u"")
        self.__ui.author.setText(u"")
        self.__ui.date.setText(u"")
