# coding: utf-8

from typing import Optional

from PySide6.QtWidgets import QTextEdit, QWidget


class ProgressBrowser(QTextEdit):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

    def update_progress(self, text: str) -> None:
        self.setText(f"{self.toPlainText()}\n{text}")


__all__ = ["ProgressBrowser"]
