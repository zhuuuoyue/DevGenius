# coding: utf-8

from typing import Union, Optional

from PySide6.QtCore import Slot, Signal, QPoint, Qt
from PySide6.QtGui import QResizeEvent, QMoveEvent, QAction
from PySide6.QtWidgets import QMainWindow, QWidget, QMenu, QMenuBar

from components import DialogBase
from .command import get_command_manager
from .WindowManager import set_main_window


class MenuItem(object):

    def __init__(self, menu_id: str, name: str, tooltip: Optional[str] = None, checked: Optional[bool] = None):
        self.menu_id: str = menu_id
        self.name: str = name
        self.tooltip: Union[str, None] = tooltip
        self.checked: Union[bool, None] = checked


class MenuGroup(object):

    def __init__(self, name: str, items: list[MenuItem]):
        self.name: str = name
        self.items: list[MenuItem] = items


class MenuAction(QAction):

    clicked = Signal(str)

    def __init__(self, menu_id: str, text: str, parent: QWidget):
        super().__init__(text=text, parent=parent)
        self.__id: str = menu_id
        super().triggered.connect(self.__on_triggered)

    @Slot()
    def __on_triggered(self) -> None:
        self.clicked.emit(self.__id)


class MainWindow(QMainWindow):

    menus: list[MenuGroup] = [
        MenuGroup(u"项目", [
            MenuItem(u"project", u"仓库管理")
        ]),
        MenuGroup(u"任务", [
            MenuItem(u"task", u"任务管理"),
            MenuItem(u"packaging", u"软件打包"),
            MenuItem(u"archive", u"软件包管理")
        ]),
        MenuGroup(u"测试", [
            MenuItem(u"analysis_test_result", u"测试分析")
        ]),
        MenuGroup(u"工具", [
            MenuItem(u"create_files", u"创建文件"),
            MenuItem(u"environment", u"环境切换")
        ]),
        MenuGroup(u"其他", [
            MenuItem(u"always_on_top", u"窗口置顶", checked=False),
            MenuItem(u"preferences", u"设置"),
            MenuItem(u"about", u"关于"),
        ]),
    ]

    def __init__(self):
        super().__init__(None)
        self.move(0, 0)
        self.setMinimumWidth(320)
        self.setFixedHeight(22)
        self.setWindowTitle(u"开发精灵 - 桌面版")

        self.menu_bar: QMenuBar = self.menuBar()
        for group in MainWindow.menus:
            menu_group: QMenu = self.menu_bar.addMenu(group.name)
            for item in group.items:
                menu_action = MenuAction(menu_id=item.menu_id, text=item.name, parent=menu_group)
                if isinstance(item.checked, bool):
                    menu_action.setCheckable(True)
                    menu_action.setChecked(item.checked)
                menu_action.clicked.connect(self.__on_menu_triggered)
                menu_group.addAction(menu_action)

        set_main_window(self)

    @Slot(str)
    def __on_menu_triggered(self, menu_id: str):
        sender = self.sender()
        if isinstance(sender, MenuAction):
            if sender.isCheckable():
                checked = sender.isChecked()
                get_command_manager().run(menu_id, checked=checked)
            else:
                get_command_manager().run(menu_id)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__update_dialog_position()

    def moveEvent(self, event: QMoveEvent) -> None:
        self.__update_dialog_position()

    def __update_dialog_position(self) -> None:
        height: int = self.frameSize().height()
        pos: QPoint = self.pos()
        DialogBase.set_default_position(QPoint(pos.x(), pos.y() + height))
