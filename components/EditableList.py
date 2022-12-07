# coding: utf-8

import os
from typing import Optional, Any

from PySide6.QtCore import Slot, Signal, QModelIndex
from PySide6.QtWidgets import QWidget, QLabel,\
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from .IconButton import IconButton
from .AdvancedList import AdvancedList, ListItemFilter
from .CustomList import ListItemFormatter, CustomList
from .SearchBar import SearchBar


class StatusBar(QLabel):

    def __init__(self, parent: Optional[QWidget] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def update_text(self, total: int, searched: Optional[int] = None) -> None:
        text = f"{total} item(s)"
        if searched is not None:
            text = f"{total} item(s), {searched} searched"
        self.setText(text)


class EditableListUI(object):

    def __init__(self, owner: QWidget):
        self.button_layout = QHBoxLayout()
        self.add_button = self.create_button(button_id="add", icon="add.png", parent=owner, tooltip=u"Add")
        self.delete_button = self.create_button(button_id="delete", icon="bin.png", parent=owner,
                                                tooltip=u"Delete the selected item(s)")
        self.delete_button.setEnabled(False)
        self.edit_button = self.create_button(button_id="edit", icon="edit.png", parent=owner,
                                              tooltip=u"Edit the selected item(s)")
        self.edit_button.setEnabled(False)
        self.button_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout.addSpacerItem(self.button_spacer)

        self.search_layout = QHBoxLayout()
        self.search_bar = SearchBar(parent=owner)
        self.search_layout.addWidget(self.search_bar)

        self.list_layout = QHBoxLayout()
        self.list = CustomList(parent=owner)
        self.list_layout.addWidget(self.list)

        self.status_layout = QHBoxLayout()
        self.status_label = StatusBar(parent=owner)
        self.status_layout.addWidget(self.status_label)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.search_layout)
        self.layout.addLayout(self.list_layout)
        self.layout.addLayout(self.status_layout)

        owner.setLayout(self.layout)

    def create_button(self, button_id: str, icon: str, tooltip: Optional[str] = None, parent: Optional[QWidget] = None):
        button = IconButton(button_id=button_id, icon=f"{os.getcwd()}\\assets\\{icon}", tooltip=tooltip, parent=parent)
        self.button_layout.addWidget(button)
        return button


class EditableList(AdvancedList):

    add_clicked = Signal()
    delete_clicked = Signal()
    edit_clicked = Signal()
    selection_changed = Signal()

    def __init__(self,
                 parent: Optional[QWidget] = None,
                 item_formatter: ListItemFormatter = None,
                 item_filter: ListItemFilter = None,
                 *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self._ui = EditableListUI(self)
        self._formatter = item_formatter
        self._filter = item_filter
        self._data: list[Any] = []

        self._ui.list.formatter = item_formatter

        self._ui.add_button.triggered.connect(self._on_add_clicked)
        self._ui.delete_button.triggered.connect(self._on_delete_clicked)
        self._ui.edit_button.triggered.connect(self._on_edit_clicked)
        self._ui.search_bar.keyword_changed.connect(self._on_keyword_changed)
        self._ui.list.itemSelectionChanged.connect(self._on_selection_changed)

        self._update_status()

    def load_data(self, items: list[Any]) -> None:
        self._data = items
        self._ui.list.load_data(items)

    def get_selected_items(self) -> list[Any]:
        indexes: list[QModelIndex] = self._ui.list.selectedIndexes()
        result: list[Any] = []
        for index in indexes:
            result.append(self._data[index.row()])
        return result

    def in_searching_mode(self):
        return self._ui.search_bar.in_searching_mode()

    def _start_searching(self):
        self._ui.add_button.setEnabled(False)
        self._ui.delete_button.setEnabled(False)
        self._ui.edit_button.setEnabled(False)

    def _end_searching(self):
        self._ui.add_button.setEnabled(True)
        self._update_buttons()

    def _update_buttons(self) -> None:
        indexes: list[QModelIndex] = self._ui.list.selectedIndexes()
        enabled = len(indexes) != 0
        self._ui.delete_button.setEnabled(enabled)
        self._ui.edit_button.setEnabled(enabled)

    def _update_status(self):
        searching = self.in_searching_mode()
        if searching:
            shown = 0
            for index in range(self._ui.list.count()):
                if not self._ui.list.isRowHidden(index):
                    shown += 1
            self._ui.status_label.update_text(len(self._data), shown)
        else:
            self._ui.status_label.update_text(len(self._data))

    @Slot()
    def _on_add_clicked(self):
        self.add_clicked.emit()

    @Slot()
    def _on_delete_clicked(self):
        self.delete_clicked.emit()

    @Slot()
    def _on_edit_clicked(self):
        self.edit_clicked.emit()

    @Slot()
    def _on_keyword_changed(self, keyword: str):
        if len(keyword) == 0:
            self._end_searching()
            for index in range(self._ui.list.count()):
                self._ui.list.setRowHidden(index, False)
        else:
            self._start_searching()
            if self._filter is not None:
                for index, item in enumerate(self._data):
                    show = self._filter.filter(item=item, keyword=keyword, items=self._data, index=index)
                    self._ui.list.setRowHidden(index, not show)
        self._update_status()

    @Slot()
    def _on_selection_changed(self):
        self._update_buttons()
        self.selection_changed.emit()


__all__ = ["EditableList"]
