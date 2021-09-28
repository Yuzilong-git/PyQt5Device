# -*- encoding: utf-8 -*-
"""
@File    : main_driver.py
@Time    : 2021/9/26 11:45
@Author  : Coco
"""
import sys

import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton, QComboBox, QFormLayout, QHeaderView

from gui.main_gui import MainWindow
from driver.visa_driver import Device


class MainAction(MainWindow):
    def __init__(self):
        super(MainAction, self).__init__()
        self._bind_actions()
        self.table = self.main_widget.table_area
        self._init()
        self.win_list = [1, 2, 3, 4]
        self.axs_list = []

    def _bind_actions(self):
        self.main_widget.plot_setting.pb_enable_1.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_enable_2.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_enable_3.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_enable_4.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_disable_1.clicked.connect(self._disable)
        self.main_widget.plot_setting.pb_disable_2.clicked.connect(self._disable)
        self.main_widget.plot_setting.pb_disable_3.clicked.connect(self._disable)
        self.main_widget.plot_setting.pb_disable_4.clicked.connect(self._disable)

    def _save_local_setting(self):
        self.widget = self.main_widget.plot_setting
        self.win_num = self.widget.cb_window.currentIndex()
        self.meas_num = self.widget.cb_measure.currentIndex()
        self.format_num = self.widget.cb_format.currentIndex()
        self.axs_list.append(self.main_widget.plot_area.ax_list[self.win_num]())
        self.main_widget.plot_area.canvas.draw()

    def _enable(self):
        # 找到所点的window序号
        sender = self.sender()
        self.select_window_num = sender.objectName()[-1]
        self.findChild(QPushButton, sender.objectName()).setEnabled(False)
        self.findChild(QPushButton, 'pb_disable_' + self.select_window_num).setEnabled(True)
        self.findChild(QComboBox, 'cb_measure_' + self.select_window_num).setEnabled(False)
        self.findChild(QComboBox, 'cb_format_' + self.select_window_num).setEnabled(False)
        # 更新活跃window列表
        self.win_list.append(int(self.select_window_num))
        self.win_list.sort()
        # 绘图部分
        plt.clf()
        self.main_widget.plot_area.canvas.draw()
        header = ["frequency"]
        for i in self.win_list:
            ax = self.main_widget.plot_area.ax_list[i - 1]()
            ax.set_xlabel("FREQ")
            ax.set_ylabel(self.main_widget.plot_setting.format_list[
                              self.findChild(QComboBox, 'cb_format_' + str(i)).currentIndex()])
            header.append(self.main_widget.plot_setting.format_list[
                              self.findChild(QComboBox, 'cb_format_' + str(i)).currentIndex()])
        self.main_widget.plot_area.canvas.draw()

        # 表格部分
        self.table.tb_content.setColumnCount(len(self.win_list) + 1)
        self.table.tb_content.setHorizontalHeaderLabels(header)

    def _disable(self):
        # 找到所点的window序号
        sender = self.sender()
        self.select_window_num = sender.objectName()[-1]
        self.main_widget.plot_setting.fl_window_1.setEnabled(False)
        self.findChild(QPushButton, sender.objectName()).setEnabled(False)
        self.findChild(QPushButton, 'pb_enable_' + self.select_window_num).setEnabled(True)
        self.findChild(QComboBox, 'cb_measure_' + self.select_window_num).setEnabled(True)
        self.findChild(QComboBox, 'cb_format_' + self.select_window_num).setEnabled(True)
        # 更新活跃window列表
        self.win_list.remove(int(self.select_window_num))
        self.win_list.sort()
        # 绘图部分
        plt.clf()
        self.main_widget.plot_area.canvas.draw()
        header = ["frequency"]
        for i in self.win_list:
            ax = self.main_widget.plot_area.ax_list[i - 1]()
            ax.set_xlabel("FREQ")
            ax.set_ylabel(self.main_widget.plot_setting.format_list[
                              self.findChild(QComboBox, 'cb_format_' + str(i)).currentIndex()])
            header.append(self.main_widget.plot_setting.format_list[
                              self.findChild(QComboBox, 'cb_format_' + str(i)).currentIndex()])
        self.main_widget.plot_area.canvas.draw()

        # 表格部分
        self.table.tb_content.setColumnCount(0)
        self.table.tb_content.setColumnCount(len(self.win_list) + 1)
        self.table.tb_content.setHorizontalHeaderLabels(header)

    def _init(self):
        for i in range(4):
            self.main_widget.plot_setting.findChild(QPushButton, 'pb_enable_' + str(i + 1)).setEnabled(False)

        for ax in self.main_widget.plot_area.ax_list:
            num = self.main_widget.plot_area.ax_list.index(ax)
            ax = ax()
            ax.set_xlabel("FREQ")
            ax.set_ylabel(self.main_widget.plot_setting.format_list[
                              self.findChild(QComboBox, 'cb_format_' + str(num + 1)).currentIndex()])

        self.main_widget.plot_area.canvas.draw()

        # 表格部分
        self.table.tb_content.setColumnCount(5)
        header = ["frequency"]
        for i in range(4):
            header.append(self.main_widget.plot_setting.format_list[i])
        self.table.tb_content.setHorizontalHeaderLabels(header)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainAction()
    window.show()
    sys.exit(app.exec_())
