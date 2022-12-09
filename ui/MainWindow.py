# coding: utf-8

import json
import os

from PySide6.QtCore import Slot, QPoint
from PySide6.QtGui import QResizeEvent, QMoveEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from components import DialogBase, ImageButton
from .command import get_command_manager
from .WindowManager import set_main_window


class MenuData(object):

    def __init__(self, menu_id: str, name: str, icon: str, tooltip: str) -> None:
        self.menu_id = menu_id
        self.name = name
        self.icon = icon
        self.tooltip = tooltip


def load_menu_configuration() -> list[MenuData]:
    with open(f"{os.getcwd()}\\configs\\main_window.json", encoding="utf-8") as fp:
        data = json.load(fp)
        configs: list[MenuData] = [MenuData(item["id"], item["name"], item["icon"], item["tooltip"]) for item in data]
    return configs


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(None)
        self.move(0, 0)
        self.setWindowTitle("DevGenius - Desktop")
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.menus: list[ImageButton] = []
        self.menu_layout = QHBoxLayout()
        menus = load_menu_configuration()
        for menu in menus:
            button = ImageButton(menu.menu_id, menu.name, menu.icon, menu.tooltip, parent=self)
            button.clicked.connect(self._on_menu_triggered)
            self.menus.append(button)
            self.menu_layout.addWidget(button)
        self.menu_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.menu_layout.addSpacerItem(self.menu_spacer)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.menu_layout)
        self.main_spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.main_layout.addSpacerItem(self.main_spacer)

        self.centralWidget.setLayout(self.main_layout)

        set_main_window(self)

    @Slot(str)
    def _on_menu_triggered(self, menu_id: str):
        get_command_manager().run(menu_id)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.__update_dialog_position()

    def moveEvent(self, event: QMoveEvent) -> None:
        self.__update_dialog_position()

    def __update_dialog_position(self) -> None:
        height: int = self.frameSize().height()
        pos: QPoint = self.pos()
        DialogBase.set_default_position(QPoint(pos.x(), pos.y() + height))
