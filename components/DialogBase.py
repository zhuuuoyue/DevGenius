# coding: utf-8

from typing import Optional, Dict, Union

from PySide6.QtCore import QSize, QPoint, QRect
from PySide6.QtGui import QMoveEvent, QResizeEvent, QGuiApplication, QScreen
from PySide6.QtWidgets import QWidget, QDialog


class DialogData(object):

    def __init__(self, sz: Optional[QSize] = None, pos: Optional[QPoint] = None):
        self.__position = QPoint(0, 0)
        self.__size = QSize(600, 400)

        self.position = pos
        self.size = sz

    def get_position(self) -> QPoint:
        return self.__position

    def set_position(self, pos: QPoint) -> None:
        if isinstance(pos, QPoint):
            self.__position = pos

    position = property(get_position, set_position)

    def get_size(self) -> QSize:
        return self.__size

    def set_size(self, sz: QSize) -> None:
        if isinstance(sz, QSize):
            self.__size = sz

    size = property(get_size, set_size)


class DialogManager(object):

    def __init__(self):
        self.__data: Dict[str, DialogData] = {}

    def has_dialog(self, dialog_id: str) -> bool:
        return dialog_id in self.__data

    def get_dialog_size(self, dialog_id: str) -> Union[QSize, None]:
        return self.__data[dialog_id].size if self.has_dialog(dialog_id) else None

    def get_dialog_position(self, dialog_id: str) -> Union[QPoint, None]:
        return self.__data[dialog_id].position if self.has_dialog(dialog_id) else None

    def update_dialog_size(self, dialog_id: str, sz: QSize) -> None:
        if self.has_dialog(dialog_id):
            self.__data[dialog_id].size = sz
        else:
            self.__data[dialog_id] = DialogData(sz=sz)

    def update_dialog_position(self, dialog_id: str, pos: QPoint) -> None:
        if self.has_dialog(dialog_id):
            self.__data[dialog_id].position = pos
        else:
            self.__data[dialog_id] = DialogData(pos=pos)


class DialogBase(QDialog):

    __manager__ = DialogManager()
    __default_position__: QPoint = QPoint(0, 0)

    def __init__(self, parent: Optional[QWidget] = None, dialog_id: Optional[str] = None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.__dialog_id: Union[str, None] = None
        if isinstance(dialog_id, str):
            self.__dialog_id = dialog_id
            if DialogBase.__manager__.has_dialog(self.dialog_id):
                self.move(DialogBase.__manager__.get_dialog_position(self.dialog_id))
                self.resize(DialogBase.__manager__.get_dialog_size(self.dialog_id))
            else:
                pos: QPoint = DialogBase.get_default_position()
                DialogBase.__manager__.update_dialog_position(self.dialog_id, pos)
                self.move(pos)

    @staticmethod
    def set_default_position(pos: QPoint) -> None:
        if isinstance(pos, QPoint):
            scrs: list[QScreen] = QGuiApplication.screens()
            max_x: int = 0
            max_y: int = 0
            for scr in scrs:
                center: QPoint = scr.geometry().center()
                if center.x() > max_x:
                    max_x = center.x()
                if center.y() > max_y:
                    max_y = center.y()
            if pos.x() > max_x or pos.y() > max_y:
                pos = QPoint(0, 0)
            DialogBase.__default_position__ = pos

    @staticmethod
    def get_default_position() -> QPoint:
        return DialogBase.__default_position__

    def get_dialog_id(self) -> Union[str, None]:
        return self.__dialog_id

    dialog_id = property(get_dialog_id)

    def moveEvent(self, event: QMoveEvent) -> None:
        if self.dialog_id is not None:
            geom: QRect = self.frameGeometry()
            DialogBase.__manager__.update_dialog_position(self.dialog_id, QPoint(geom.x(), geom.y()))

    def resizeEvent(self, event: QResizeEvent) -> None:
        if self.dialog_id is not None:
            DialogBase.__manager__.update_dialog_size(self.dialog_id, event.size())


__all__ = ["DialogBase"]
