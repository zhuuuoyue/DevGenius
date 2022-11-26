# coding: utf-8

from typing import Optional, Sequence
import logging
import json
import os

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from .widgets.MenuButton import MenuButton
from .command import get_command_manager
from .WindowManager import get_window_manager


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
        self.setWindowTitle("DevGenius")
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.menus: list[MenuButton] = []
        self.menu_layout = QHBoxLayout()
        menus = load_menu_configuration()
        for menu in menus:
            button = MenuButton(menu.menu_id, menu.name, menu.icon, menu.tooltip, parent=self)
            button.triggered.connect(self._on_menu_triggered)
            self.menus.append(button)
            self.menu_layout.addWidget(button)
        self.menu_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.menu_layout.addSpacerItem(self.menu_spacer)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.menu_layout)
        self.main_spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.main_layout.addSpacerItem(self.main_spacer)

        self.centralWidget.setLayout(self.main_layout)

        get_window_manager().register_main_window(self)

    @Slot(str)
    def _on_menu_triggered(self, menu_id: str):
        get_command_manager().run(menu_id)
