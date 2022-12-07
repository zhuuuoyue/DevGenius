# coding: utf-8

import os
from typing import Optional

from PySide6.QtCore import QMargins
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QSpacerItem, QSizePolicy

from components import WidgetBase, ImageButton


class EnvironmentButton(ImageButton):

    def __init__(self, button_id: str, name: str, icon: str, parent: Optional[QWidget] = None, *args, **kwargs):
        icon_path = f"{os.getcwd()}\\assets\\environment_icons\\{icon}"
        super().__init__(button_id=button_id, name=name, icon=icon_path, parent=parent, *args, **kwargs)


class EnvironmentSelectorUI(object):

    def __init__(self, owner: QWidget):
        self.left_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.env_qa = EnvironmentButton(button_id=u"qa", name=u"QA", icon=u"li_sheng_su.png", parent=owner)
        self.env_c = EnvironmentButton(button_id=u"c", name=u"C", icon=u"wang_yan.png", parent=owner)
        self.env_product = EnvironmentButton(button_id=u"product", name=u"Product", icon=u"chi_xiao_qiu.png", parent=owner)
        self.env_product_2 = EnvironmentButton(button_id=u"product-2", name=u"Product II", icon=u"zhang_jia_chun.png", parent=owner)
        self.right_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)

        self.inner_layout = QHBoxLayout()
        self.inner_layout.setContentsMargins(4, 24, 4, 24)
        self.inner_layout.addSpacerItem(self.left_spacer)
        self.inner_layout.addWidget(self.env_qa)
        self.inner_layout.addWidget(self.env_c)
        self.inner_layout.addWidget(self.env_product)
        self.inner_layout.addWidget(self.env_product_2)
        self.inner_layout.addSpacerItem(self.right_spacer)

        self.group = QGroupBox(title=u"Select environment", parent=owner)
        self.group.setLayout(self.inner_layout)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.group)

        owner.setLayout(self.layout)


class EnvironmentSelector(WidgetBase):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self.ui = EnvironmentSelectorUI(self)
