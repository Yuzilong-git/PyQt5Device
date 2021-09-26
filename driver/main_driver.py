# -*- encoding: utf-8 -*-
"""
@File    : main_driver.py
@Time    : 2021/9/26 11:45
@Author  : Coco
"""
import sys

from PyQt5.QtWidgets import QMessageBox, QApplication

from gui.main_gui import MainWindow


class MainAction(MainWindow):
    def __init__(self):
        super(MainAction, self).__init__()
        self._bind_actions()

    def _bind_actions(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
