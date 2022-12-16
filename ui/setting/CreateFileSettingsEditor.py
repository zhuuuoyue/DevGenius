# coding: utf-8

from typing import Optional
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QSpacerItem, QSizePolicy

from concepts.setting import FileAuthors
from components import WidgetBase, Form, FormRowInfo
from bussiness.setting import get_authors, set_authors

from .ISettingEditor import ISettingEditor


class CreateFileSettingsEditorUI(object):

    def __init__(self, owner: QWidget):
        self.owner_input = QLineEdit(parent=owner)
        self.co_owner_input = QLineEdit(parent=owner)
        self.form = Form(
            [
                FormRowInfo(title=u"Owner", value=self.owner_input),
                FormRowInfo(title=u"Co-Owner", value=self.co_owner_input),
            ],
            parent=owner
        )
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.form)
        self.spacer = QSpacerItem(0, 0, vData=QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.spacer)
        owner.setLayout(self.layout)


class CreateFileSettingsEditor(WidgetBase, ISettingEditor):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__ui = CreateFileSettingsEditorUI(self)

        authors = get_authors()
        self.load_data(authors)

    def load_data(self, authors: FileAuthors) -> None:
        self.__ui.owner_input.setText(authors.owner)
        self.__ui.co_owner_input.setText(authors.co_owner)

    def apply_modification(self, *args, **kwargs) -> None:
        set_authors(FileAuthors(
            owner=self.__ui.owner_input.text(),
            co_owner=self.__ui.co_owner_input.text()
        ))
