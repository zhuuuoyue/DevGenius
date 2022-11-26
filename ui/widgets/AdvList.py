# coding: utf-8

from typing import Optional, Any
from abc import ABC, abstractmethod

from PySide6.QtCore import Qt, QSize, Slot, Signal, QModelIndex
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QListWidget, QLabel,\
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from .WidgetBase import WidgetBase


class AdvListUI(object):

    def __init__(self, owner: QWidget):
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton(parent=owner)
        self._init_button(self.add_button, u"A", u"添加")
        self.delete_button = QPushButton(parent=owner)
        self._init_button(self.delete_button, u"D", u"删除")
        self.edit_button = QPushButton(parent=owner)
        self._init_button(self.edit_button, u"M", u"修改")
        self.button_spacer = QSpacerItem(0, 0, hData=QSizePolicy.Policy.Expanding)
        self.button_layout.addSpacerItem(self.button_spacer)

        self.search_layout = QHBoxLayout()
        self.keyword_input = QLineEdit(parent=owner)
        self.keyword_input.setPlaceholderText(u"输入关键字，开始搜索 ...")
        self.keyword_input.setClearButtonEnabled(True)
        self.search_layout.addWidget(self.keyword_input)

        self.list_layout = QHBoxLayout()
        self.list = QListWidget(parent=owner)
        self.list_layout.addWidget(self.list)

        self.status_layout = QHBoxLayout()
        self.status_label = QLabel(parent=owner)
        self.status_layout.addWidget(self.status_label)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.search_layout)
        self.layout.addLayout(self.list_layout)
        self.layout.addLayout(self.status_layout)

        owner.setLayout(self.layout)

    def _init_button(self, button: QPushButton, text: str, tooltip: str = None):
        button.setText(text)
        if tooltip is not None:
            button.setToolTip(tooltip)
        button.setFixedSize(QSize(24, 24))
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_layout.addWidget(button)


class AdvListItemFormatter(ABC):

    @abstractmethod
    def format(self, item: Any, items: list[Any] = None, index: Optional[int] = None) -> str:
        pass


class AdvListItemSorter(ABC):

    @abstractmethod
    def run(self, lhs: Any, rhs: Any) -> bool:
        pass


class AdvListItemFilter(ABC):

    @abstractmethod
    def filter(self, item: Any, keyword: str, items: list[Any] = None, index: Optional[int] = None) -> bool:
        pass


class AdvList(WidgetBase):

    add_clicked = Signal()
    delete_clicked = Signal()
    edit_clicked = Signal()
    selection_changed = Signal()

    def __init__(self,
                 parent: Optional[QWidget] = None,
                 formatter: AdvListItemFormatter = None,
                 sorter: AdvListItemSorter = None,
                 filter: AdvListItemFilter = None,
                 *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self._ui = AdvListUI(self)
        self._formatter = formatter
        self._sorter = sorter
        self._filter = filter
        self._data: list[Any] = []

        self._ui.add_button.clicked.connect(self._on_add_clicked)
        self._ui.delete_button.clicked.connect(self._on_delete_clicked)
        self._ui.edit_button.clicked.connect(self._on_edit_clicked)
        self._ui.keyword_input.textChanged.connect(self._on_keyword_changed)
        self._ui.list.itemSelectionChanged.connect(self._on_selection_changed)

        self._update_status()

    def load_data(self, items: list[Any]) -> None:
        if self._formatter is None:
            return
        self._data = items
        for index, item in enumerate(items):
            text = self._formatter.format(item=item, items=items, index=index)
            self._ui.list.addItem(text)

    def get_selected_project(self) -> Optional[Any]:
        indexes: list[QModelIndex] = self._ui.list.selectedIndexes()
        selected = len(indexes)
        if selected == 0 or selected >= len(self._data):
            return
        return self._data[indexes[0].row()]

    def in_searching_mode(self):
        return len(self._ui.keyword_input.text()) != 0

    def _start_searching(self):
        self._ui.add_button.setEnabled(False)
        self._ui.delete_button.setEnabled(False)
        self._ui.edit_button.setEnabled(False)

    def _end_searching(self):
        self._ui.add_button.setEnabled(True)
        self._ui.delete_button.setEnabled(True)
        self._ui.edit_button.setEnabled(True)

    def _update_status(self):
        searching = self.in_searching_mode()
        if searching:
            shown = 0
            for index in range(self._ui.list.count()):
                if not self._ui.list.isRowHidden(index):
                    shown += 1
            text = f"共 {len(self._data)} 项，搜索到 {shown} 项"
        else:
            text = f"共 {len(self._data)} 项"
        self._ui.status_label.setText(text)

    @Slot()
    def _on_add_clicked(self):
        pass

    @Slot()
    def _on_delete_clicked(self):
        pass

    @Slot()
    def _on_edit_clicked(self):
        pass

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
        self.selection_changed.emit()
