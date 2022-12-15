# coding: utf-8

import os
from typing import Optional, Union

from PySide6.QtCore import QSize, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy

from concepts.test import TestCaseRunningResultCollection, TestCaseRunningResult
from bussiness.TestUtils import parse_test_results
from components import WindowBase, WidgetBase

from .TestResultTable import TestResultTable
from .TestRunningInfoPanel import TestRunningInfoPanel
from .TestErrorInfoPanel import TestErrorInfoPanel
from .TestCaseInfoPanel import TestCaseInfoPanel


class TestWindowCentralWidget(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        right_panel_width: int = 320

        self.result_table = TestResultTable(self)

        self.running_info_panel = TestRunningInfoPanel(self)

        self.error_info_panel = TestErrorInfoPanel(self)
        self.error_info_panel.setFixedWidth(right_panel_width)

        self.case_info_panel = TestCaseInfoPanel(self)
        self.case_info_panel.setFixedWidth(right_panel_width)

        self.left_layout = QVBoxLayout()
        self.left_layout.setSpacing(8)
        self.left_layout.addWidget(self.running_info_panel)
        self.left_layout.addWidget(self.result_table)

        self.right_layout = QVBoxLayout()
        self.right_layout.setSpacing(12)
        self.right_layout.setContentsMargins(4, 4, 4, 4)
        self.right_layout.addWidget(self.error_info_panel)
        self.right_layout.addWidget(self.case_info_panel)
        self.right_bottom_spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.right_layout.addSpacerItem(self.right_bottom_spacer)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)


class TestWindowUI(object):

    def __init__(self, win: QMainWindow):
        win.setWindowTitle(u"测试")
        win.setMinimumSize(QSize(1200, 860))
        win.move(0, 0)

        self.menu_bar = win.menuBar()

        self.file_menu = self.menu_bar.addMenu(u"文件")
        self.open_action = QAction(u"打开文件夹")
        self.file_menu.addAction(self.open_action)
        self.close_action = QAction(u"关闭文件夹")
        self.file_menu.addAction(self.close_action)
        self.file_menu.addSeparator()
        self.exit_action = QAction(u"退出")
        self.file_menu.addAction(self.exit_action)

        self.table_menu = self.menu_bar.addMenu(u"表格")
        self.adjust_column_width_action = QAction(u"调整表格列宽")
        self.table_menu.addAction(self.adjust_column_width_action)

        self.central_widget = TestWindowCentralWidget(win)
        win.setCentralWidget(self.central_widget)

    def add_table_column(self, text: str) -> QAction:
        action = QAction(text)
        action.setCheckable(True)
        self.table_menu.addAction(action)
        return action


class TestWindow(WindowBase):

    __cache_open_directory: Union[str, None] = None

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent)
        self.__ui = TestWindowUI(self)
        self.__ui.central_widget.running_info_panel.set_data(TestCaseRunningResultCollection())

        self.__ui.open_action.triggered.connect(self.__on_open_clicked)
        self.__ui.adjust_column_width_action.triggered.connect(self.__on_adjust_table_column_width_clicked)

        self.__ui.central_widget.result_table.selectedTestCaseChanged.connect(self.__on_selected_test_case_changed)

    @Slot(bool)
    def __on_open_clicked(self) -> None:
        test_output_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption=u"请选择测试输出文件夹",
            dir=os.getcwd() if TestWindow.__cache_open_directory is None else TestWindow.__cache_open_directory
        )
        if not os.path.isdir(test_output_dir):
            return
        TestWindow.__cache_open_directory = test_output_dir
        result_collection = parse_test_results(test_output_dir=test_output_dir)
        self.__ui.central_widget.result_table.load_data(result_collection)
        self.__ui.central_widget.running_info_panel.set_data(result_collection)

    @Slot()
    def __on_adjust_table_column_width_clicked(self) -> None:
        self.__ui.central_widget.result_table.adjust_column_width()

    @Slot()
    def __on_selected_test_case_changed(self) -> None:
        test_case_result = self.__ui.central_widget.result_table.get_selected_test_case()
        if isinstance(test_case_result, TestCaseRunningResult):
            self.__ui.central_widget.error_info_panel.set_data(test_case_result.error_info)
            self.__ui.central_widget.case_info_panel.set_data(test_case_result.test_case)
