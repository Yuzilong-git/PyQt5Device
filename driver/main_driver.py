# -*- encoding: utf-8 -*-
"""
@File    : main_driver.py
@Time    : 2021/9/26 11:45
@Author  : Coco
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton, QComboBox

from gui.main_gui import MainWindow
from driver.visa_driver import Device


class MainAction(MainWindow):
    def __init__(self):
        super(MainAction, self).__init__()
        self._bind_actions()
        self.table = self.main_widget.table_area
        self.device = Device()
        self.device.set_external_mode()
        self._init()
        self.win_list = [1, 2, 3, 4]
        self.format_list = ['MLOGarithmic', 'MLINear', 'PHASe', 'POLar']
        self.axs_list = self.main_widget.plot_area.ax_list

    def _bind_actions(self):
        self.main_widget.plot_setting.pb_enable_1.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_enable_2.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_enable_3.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_enable_4.clicked.connect(self._enable)
        self.main_widget.plot_setting.pb_disable_1.clicked.connect(self._disable)
        self.main_widget.plot_setting.pb_disable_2.clicked.connect(self._disable)
        self.main_widget.plot_setting.pb_disable_3.clicked.connect(self._disable)
        self.main_widget.plot_setting.pb_disable_4.clicked.connect(self._disable)
        self.main_widget.global_setting.pb_save_global_setting.clicked.connect(self._save_global_setting)
        self.main_widget.global_setting.pb_plot.clicked.connect(self._plot_and_fill)

    def _plot_and_fill(self):
        win_data_dict = {0: self.device.get_x_data()}
        # 获取窗口横坐标
        # 获取活跃窗口的纵坐标
        for win_num in self.win_list:
            win_data_dict[win_num] = self.device.get_y_data(win_num)

        for win_num in self.win_list:
            cb_format = self.findChild(QComboBox, 'cb_format_' + str(win_num))
            if cb_format.currentIndex() != 3 and cb_format.currentIndex() != 4:
                print('X >>>>>>>>>>>>>>\n', win_data_dict[0], "\n\n", "y>>>>>>>>>>>>>>>>\n", win_data_dict[win_num])
                self.main_widget.plot_area.ax_list[win_num - 1]().plot(win_data_dict[0], win_data_dict[win_num])
        self.main_widget.plot_area.canvas.draw()

    def _save_local_setting(self):
        self.widget = self.main_widget.plot_setting
        self.win_num = self.widget.cb_window.currentIndex()
        self.meas_num = self.widget.cb_measure.currentIndex()
        self.format_num = self.widget.cb_format.currentIndex()
        self.axs_list.append(self.main_widget.plot_area.ax_list[self.win_num]())
        self.main_widget.plot_area.canvas.draw()

    def _save_global_setting(self):
        global_setting_list = self._data_processing()
        if global_setting_list:
            start_freq, stop_freq, center_freq, points_data = global_setting_list
            self.device.set_sweep_parameter(start_freq, stop_freq, center_freq, points_data)

    def _enable(self):
        # 找到所点的window序号
        sender = self.sender()
        self.select_window_num = sender.objectName()[-1]
        cb_measure = self.findChild(QComboBox, 'cb_measure_' + self.select_window_num)
        cb_format = self.findChild(QComboBox, 'cb_format_' + self.select_window_num)
        mode = self.main_widget.plot_setting.format_list[cb_format.currentIndex()]
        if mode in self.format_list:
            QMessageBox.critical(self, "错误", "该format已存在，请重新选择")
            return
        self.findChild(QPushButton, sender.objectName()).setEnabled(False)
        self.findChild(QPushButton, 'pb_disable_' + self.select_window_num).setEnabled(True)
        cb_measure.setEnabled(False)
        cb_format.setEnabled(False)
        # 更新活跃window列表
        self.win_list.append(int(self.select_window_num))
        self.win_list.sort()
        # 设备窗口添加
        window_num = self.select_window_num
        mode = self.main_widget.plot_setting.format_list[cb_format.currentIndex()]
        self.device.create_window(window_num, mode)
        # 更新设备格式列表
        self.format_list.append(self.main_widget.plot_setting.format_list[cb_format.currentIndex()])
        # print(self.format_list)
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
        # 数字 1 - 4
        self.select_window_num = sender.objectName()[-1]
        cb_measure = self.findChild(QComboBox, 'cb_measure_' + self.select_window_num)
        cb_format = self.findChild(QComboBox, 'cb_format_' + self.select_window_num)
        self.main_widget.plot_setting.fl_window_1.setEnabled(False)
        self.findChild(QPushButton, sender.objectName()).setEnabled(False)
        self.findChild(QPushButton, 'pb_enable_' + self.select_window_num).setEnabled(True)
        cb_measure.setEnabled(True)
        cb_format.setEnabled(True)
        # 更新活跃window列表
        self.win_list.remove(int(self.select_window_num))
        self.win_list.sort()
        # 设备窗口删除
        self.device.del_window(self.select_window_num)
        # 更新设备格式列表
        self.format_list.remove(self.main_widget.plot_setting.format_list[cb_format.currentIndex()])
        # print(self.format_list)
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

        # 设备初始化
        self.device.set_external_mode()
        self.device.preset()
        self.device.create_window(2, 'MLINear')
        self.device.create_window(3, 'PHASe')
        self.device.create_window(4, 'POLar')
        # self.device.set_external_mode()

    def _data_processing(self):
        # 重定义
        self.global_win = self.main_widget.global_setting

        # 获取输入值
        start_freq = self.global_win.le_start.text()
        stop_freq = self.global_win.le_stop.text()
        center_freq = self.global_win.le_center.text()
        points_data = self.global_win.le_points.text()

        # 检测是否输入
        if start_freq == '' or stop_freq == '' or center_freq == '' or points_data == '':
            QMessageBox.critical(self, "错误", "存在未输入全局参数")
            return

        # 获取输入单位
        start_unit = self.global_win.cb_start_unit.currentIndex()
        stop_unit = self.global_win.cb_stop_unit.currentIndex()
        center_unit = self.global_win.cb_center_unit.currentIndex()
        # 频率单位换算
        start_freq_pow = pow(1000, int(start_unit) + 1)
        start_freq = float(start_freq) * start_freq_pow
        stop_freq_pow = pow(1000, int(stop_unit) + 1)
        stop_freq = float(stop_freq) * stop_freq_pow
        center_freq_pow = pow(1000, int(center_unit) + 1)
        center_freq = float(center_freq) * center_freq_pow
        points_data = int(points_data)

        # 输入值范围合法性校验
        if start_freq < 100000 or stop_freq < 100000:
            QMessageBox.critical(self, "错误", "起始频率或截止频率输入值过低")
            return
        if start_freq > 26500000000 or stop_freq > 26500000000:
            QMessageBox.critical(self, '错误', "起始频率或截止频率输入值过高")
            return
        if start_freq >= stop_freq:
            QMessageBox.critical(self, '错误', "起始频率应小于截止频率")
            return
        if center_freq > stop_freq or center_freq < start_freq:
            QMessageBox.critical(self, '错误', "中频带宽应介于起始频率与截止频率之间")
            return
        if points_data < 0 or points_data > 10000:
            QMessageBox.critical(self, '错误', "扫描点数输入不合法")
            return
        QMessageBox.information(self, "成功", "参数设置成功")
        return [start_freq, stop_freq, center_freq, points_data]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainAction()
    window.show()
    sys.exit(app.exec_())
