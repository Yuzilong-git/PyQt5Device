# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    : 2021/9/26 11:41
@Author  : Coco
"""
import sys
from driver.main_driver import MainAction

from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainAction()
    window.show()
    sys.exit(app.exec_())
