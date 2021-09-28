# -*- encoding: utf-8 -*-
"""
@File    : main_gui.py
@Time    : 2021/9/26 11:45
@Author  : Coco
"""
import sys

import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QMainWindow, QComboBox, QHeaderView, QTableWidget, QAbstractItemView, QFormLayout, QFrame, QSplitter


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = MainWidget()
        self.setWindowTitle("KEYSIGHT   E5080B")
        self.resize(1370, 872)
        with open('../QSS/origin.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        self._setupUI()

    def _setupUI(self):
        self.setCentralWidget(self.main_widget)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.plot_setting = PlotSetting()
        self.global_setting = GlobalSetting()
        self.plot_area = PlotArea()
        self.table_area = TableArea()
        self._setupUI()

    def _setupUI(self):
        self.hl_main = QHBoxLayout(self)

        self.vl_left = QVBoxLayout()
        self.vl_left.addWidget(self.plot_area)
        self.vl_left.addWidget(self.table_area)
        self.vl_left.setStretch(0, 3)
        self.vl_left.setStretch(1, 2)

        self.vl_right = QVBoxLayout()
        self.vl_right.addWidget(self.plot_setting)
        self.vl_right.addWidget(self.global_setting)
        self.vl_right.setStretch(0, 6)
        self.vl_right.setStretch(1, 4)

        self.hl_main.addLayout(self.vl_left)
        self.hl_main.addLayout(self.vl_right)
        self.hl_main.setStretch(0, 6)
        self.hl_main.setStretch(1, 4)


class PlotSetting(QWidget):
    """   Function: 画图的参数设置，包括每个window的参数   """

    def __init__(self):
        super(PlotSetting, self).__init__()
        self._setupUI()

    def _setupUI(self):
        # 参数选择列表
        self.measure_list = ['S11', 'S21', 'S12', 'S22']
        self.format_list = ['MLOGarithmic', 'MLINear', 'PHASe', 'POLar', 'SMITh', 'SWR', 'REAL', 'IMAGinary', 'GDELay',
                            'UPHase', 'PPHase']
        # 整体采用垂直布局
        self.vl_plot_setting = QVBoxLayout(self)
        self.vl_plot_setting.setSpacing(20)
        # 1、2窗口的水平布局
        self.hl_window_12 = QHBoxLayout()
        # 3、4窗口的水平布局
        self.hl_window_34 = QHBoxLayout()

        # window 1
        self.frame_win1 = QFrame()  # 创建一个frame对象
        self.frame_win1.resize(3100, 3300)
        self.frame_win1.setStyleSheet('background-color:#CFCFCF;')  # 设置背景色
        self.frame_win1.setFrameShape(QFrame.Panel)

        # 每个图形的参数设置采用表单布局
        self.fl_window_1 = QFormLayout(self.frame_win1)
        self.fl_window_1.setVerticalSpacing(20)
        # window 选择栏
        self.lb_window_1 = QLabel("Window1")
        # 测量参数选择栏
        self.lb_measure_1 = QLabel("Measure:")
        self.cb_measure_1 = QComboBox()
        self.cb_measure_1.setEnabled(False)
        self.cb_measure_1.setObjectName("cb_measure_1")
        self.cb_measure_1.addItems(self.measure_list)
        self.cb_measure_1.setCurrentIndex(0)
        # 属性选择栏
        self.lb_format_1 = QLabel("Format:")
        self.cb_format_1 = QComboBox()
        self.cb_format_1.setEnabled(False)
        self.cb_format_1.setObjectName("cb_format_1")
        self.cb_format_1.addItems(self.format_list)
        self.cb_format_1.setCurrentIndex(0)
        self.pb_enable_1 = QPushButton("Enable")
        self.pb_enable_1.setObjectName("pb_enable_1")
        self.pb_disable_1 = QPushButton("Disable")
        self.pb_disable_1.setObjectName("pb_disable_1")

        # 添加到网格中
        self.fl_window_1.addRow(self.lb_window_1)
        self.fl_window_1.addRow(self.lb_measure_1, self.cb_measure_1)
        self.fl_window_1.addRow(self.lb_format_1, self.cb_format_1)
        self.fl_window_1.addRow(self.pb_enable_1, self.pb_disable_1)

        # window 2
        self.frame_win2 = QFrame()  # 创建一个frame对象
        self.frame_win2.resize(3100, 3300)
        self.frame_win2.setStyleSheet('background-color:#CFCFCF;')  # 设置背景色
        self.frame_win2.setFrameShape(QFrame.Panel)

        self.fl_window_2 = QFormLayout(self.frame_win2)
        self.fl_window_2.setVerticalSpacing(20)
        # window 选择栏
        self.lb_window_2 = QLabel("Window2")
        # 测量参数选择栏
        self.lb_measure_2 = QLabel("Measure:")
        self.cb_measure_2 = QComboBox()
        self.cb_measure_2.setEnabled(False)
        self.cb_measure_2.setObjectName("cb_measure_2")
        self.cb_measure_2.addItems(self.measure_list)
        self.cb_measure_2.setCurrentIndex(1)
        # 属性选择栏
        self.lb_format_2 = QLabel("Format:")
        self.cb_format_2 = QComboBox()
        self.cb_format_2.setEnabled(False)
        self.cb_format_2.setObjectName("cb_format_2")
        self.cb_format_2.addItems(self.format_list)
        self.cb_format_2.setCurrentIndex(1)

        self.pb_enable_2 = QPushButton("Enable")
        self.pb_enable_2.setObjectName("pb_enable_2")
        self.pb_disable_2 = QPushButton("Disable")
        self.pb_disable_2.setObjectName("pb_disable_2")

        self.fl_window_2.addRow(self.lb_window_2)
        self.fl_window_2.addRow(self.lb_measure_2, self.cb_measure_2)
        self.fl_window_2.addRow(self.lb_format_2, self.cb_format_2)
        self.fl_window_2.addRow(self.pb_enable_2, self.pb_disable_2)

        # window 3
        self.frame_win3 = QFrame()  # 创建一个frame对象
        self.frame_win3.resize(3100, 3300)
        self.frame_win3.setStyleSheet('background-color:#CFCFCF;')  # 设置背景色
        self.frame_win3.setFrameShape(QFrame.Panel)

        self.fl_window_3 = QFormLayout(self.frame_win3)
        self.fl_window_3.setVerticalSpacing(20)
        # window 选择栏
        self.lb_window_3 = QLabel("Window3")
        # 测量参数选择栏
        self.lb_measure_3 = QLabel("Measure:")
        self.cb_measure_3 = QComboBox()
        self.cb_measure_3.setEnabled(False)
        self.cb_measure_3.setObjectName("cb_measure_3")
        self.cb_measure_3.addItems(self.measure_list)
        self.cb_measure_3.setCurrentIndex(2)
        # 属性选择栏
        self.lb_format_3 = QLabel("Format:")
        self.cb_format_3 = QComboBox()
        self.cb_format_3.setEnabled(False)
        self.cb_format_3.setObjectName("cb_format_3")
        self.cb_format_3.addItems(self.format_list)
        self.cb_format_3.setCurrentIndex(2)

        self.pb_enable_3 = QPushButton("Enable")
        self.pb_enable_3.setObjectName("pb_enable_3")
        self.pb_disable_3 = QPushButton("Disable")
        self.pb_disable_3.setObjectName("pb_disable_3")

        self.fl_window_3.addRow(self.lb_window_3)
        self.fl_window_3.addRow(self.lb_measure_3, self.cb_measure_3)
        self.fl_window_3.addRow(self.lb_format_3, self.cb_format_3)
        self.fl_window_3.addRow(self.pb_enable_3, self.pb_disable_3)

        # window 4
        self.frame_win4 = QFrame()  # 创建一个frame对象
        self.frame_win4.resize(3100, 3300)
        self.frame_win4.setStyleSheet('background-color:#CFCFCF;')  # 设置背景色
        self.frame_win4.setFrameShape(QFrame.Panel)

        self.fl_window_4 = QFormLayout(self.frame_win4)
        self.fl_window_4.setVerticalSpacing(20)
        # window 选择栏
        self.lb_window_4 = QLabel("Window4")
        # 测量参数选择栏
        self.lb_measure_4 = QLabel("Measure:")
        self.cb_measure_4 = QComboBox()
        self.cb_measure_4.setEnabled(False)
        self.cb_measure_4.setObjectName("cb_measure_4")
        self.cb_measure_4.addItems(self.measure_list)
        self.cb_measure_4.setCurrentIndex(3)
        # 属性选择栏
        self.lb_format_4 = QLabel("Format:")
        self.cb_format_4 = QComboBox()
        self.cb_format_4.setEnabled(False)
        self.cb_format_4.setObjectName("cb_format_4")
        self.cb_format_4.addItems(self.format_list)
        self.cb_format_4.setCurrentIndex(3)

        self.pb_enable_4 = QPushButton("Enable")
        self.pb_enable_4.setObjectName("pb_enable_4")
        self.pb_disable_4 = QPushButton("Disable")
        self.pb_disable_4.setObjectName("pb_disable_4")

        self.fl_window_4.addRow(self.lb_window_4)
        self.fl_window_4.addRow(self.lb_measure_4, self.cb_measure_4)
        self.fl_window_4.addRow(self.lb_format_4, self.cb_format_4)
        self.fl_window_4.addRow(self.pb_enable_4, self.pb_disable_4)

        # 将1、2， 3、4窗口分别添加到布局中
        self.hl_window_12.addWidget(self.frame_win1)
        self.hl_window_12.addWidget(self.frame_win2)
        self.hl_window_34.addWidget(self.frame_win3)
        self.hl_window_34.addWidget(self.frame_win4)

        # 保存设置按钮
        # 将窗口父级添加到局部设置窗口中
        self.vl_plot_setting.addStretch(1)
        self.vl_plot_setting.addLayout(self.hl_window_12)
        self.vl_plot_setting.addLayout(self.hl_window_34)
        self.vl_plot_setting.addStretch(15)


class GlobalSetting(QWidget):
    """   Function: 全局的参数设置，包括所有window的频率、点数等参数设置   """

    def __init__(self):
        super(GlobalSetting, self).__init__()
        self._setupUI()

    def _setupUI(self):
        self.vl_global_setting = QVBoxLayout(self)
        frame = QFrame()  # 创建一个frame对象
        frame.resize(3100, 3300)
        frame.setStyleSheet('background-color:#CFCFCF;')  # 设置背景色
        frame.setFrameShape(QFrame.Panel)

        self.gl_global_setting = QGridLayout(frame)
        self.gl_global_setting.setHorizontalSpacing(30)
        self.gl_global_setting.setVerticalSpacing(20)

        self.lb_blank = QLabel('')
        self.unit_list = ['KHz', 'MHz', 'GHz']
        self.lb_start = QLabel("起始频率：")
        self.le_start = QLineEdit()
        self.cb_start_unit = QComboBox()
        self.cb_start_unit.addItems(self.unit_list)
        self.lb_stop = QLabel("截止频率：")
        self.le_stop = QLineEdit()
        self.cb_stop_unit = QComboBox()
        self.cb_stop_unit.addItems(self.unit_list)
        self.lb_center = QLabel("中频带宽：")
        self.le_center = QLineEdit()
        self.cb_center_unit = QComboBox()
        self.cb_center_unit.addItems(self.unit_list)
        self.lb_points = QLabel("扫描点数：")
        self.le_points = QLineEdit()
        self.cb_points = QComboBox()
        self.cb_points.setEnabled(False)
        self.pb_save_global_setting = QPushButton('保存设置')
        self.pb_plot = QPushButton("绘制")
        self.pb_clear = QPushButton("清除")

        self.gl_global_setting.addWidget(self.lb_start, 0, 1)
        self.gl_global_setting.addWidget(self.le_start, 0, 2)
        self.gl_global_setting.addWidget(self.cb_start_unit, 0, 3)
        self.gl_global_setting.addWidget(self.lb_stop, 1, 1)
        self.gl_global_setting.addWidget(self.le_stop, 1, 2)
        self.gl_global_setting.addWidget(self.cb_stop_unit, 1, 3)
        self.gl_global_setting.addWidget(self.lb_center, 2, 1)
        self.gl_global_setting.addWidget(self.le_center, 2, 2)
        self.gl_global_setting.addWidget(self.cb_center_unit, 2, 3)
        self.gl_global_setting.addWidget(self.lb_points, 3, 1)
        self.gl_global_setting.addWidget(self.le_points, 3, 2)
        self.gl_global_setting.addWidget(self.cb_points, 3, 3)
        self.gl_global_setting.addWidget(self.pb_save_global_setting, 4, 2)
        self.gl_global_setting.addWidget(self.pb_plot, 5, 2)
        self.gl_global_setting.addWidget(self.pb_clear, 5, 1)
        self.gl_global_setting.addWidget(self.lb_blank, 6, 4)
        self.vl_global_setting.addWidget(frame)


class PlotArea(QWidget):
    """   Function: 画图区域设计   """

    def __init__(self):
        super(PlotArea, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.ax = []
        self._setupUI()

    def _setupUI(self):
        self.figure = plt.figure()
        self.figure.subplots_adjust(wspace=0.3, hspace=0.3, top=0.95, right=0.95, left=0.1)  # 调整子图间距
        self.canvas = FigureCanvas(self.figure)

        self.ax_list = [self._create_ax(221), self._create_ax(222), self._create_ax(223), self._create_ax(224)]
        # 设置布局
        self.vl_plot = QVBoxLayout(self)
        self.vl_plot.addWidget(self.canvas)

    def _create_ax(self, position):
        def inner():
            self.ax = self.figure.add_subplot(position)
            return self.ax

        return inner


class TableArea(QWidget):
    """   Function: 表格区域设计   """

    def __init__(self):
        super(TableArea, self).__init__()
        self._setupUI()

    def _setupUI(self):
        # 横向布局
        self.vl_content = QVBoxLayout(self)
        # 创建一个表格
        self.tb_content = QTableWidget()
        self.tb_content.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_content.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.vl_content.addWidget(self.tb_content)  # 把表格加入布局


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
