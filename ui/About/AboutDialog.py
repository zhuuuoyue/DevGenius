# coding: utf-8

import os
from typing import Optional, Tuple

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from components import DialogBase, ImageLabel


class AboutDialog(DialogBase):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setWindowTitle(u"About")
        self.setFixedSize(QSize(600, 404))

        image_path = f"{os.getcwd()}\\assets\\images\ding_jun_shan.png"
        self.image = ImageLabel(image_path, parent=self)

        self.right_layout = QVBoxLayout()
        self.right_layout.setSpacing(8)
        self.name_title, self.name, self.name_layout = self.add_row(u"Name", u"DevGenius")
        self.author_title, self.author, self.author_layout = self.add_row(u"Author", u"zhuoy")
        self.mail_title, self.mail, self.mail_layout = self.add_row(u"Mail", u"zhuoyue_cn@yeah.net")
        self.repository_title, self.repository, self.repository_layout = self.add_row(u"Repository", u"https://github.com")

        self.right_spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.right_layout.addSpacerItem(self.right_spacer)

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(32)
        self.main_layout.addWidget(self.image)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

        self.setStyleSheet("""
        .ImageLabel {
        border: 1px solid gray;
        }
        """)

    def add_row(self, title_text: str, value_text: str) -> Tuple[QLabel, QLineEdit, QHBoxLayout]:
        title = QLabel(text=title_text, parent=self)
        title.setFixedWidth(60)

        value = QLineEdit(parent=self)
        value.setText(value_text)
        value.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        value.setDisabled(True)

        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(value)
        layout.setSpacing(8)

        self.right_layout.addLayout(layout)
        return title, value, layout
