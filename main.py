# coding: utf-8

import sys

from PySide6.QtWidgets import QApplication

from db import create_tables_if_not_exist
from ui import MainWindow

if __name__ == "__main__":
    create_tables_if_not_exist()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
