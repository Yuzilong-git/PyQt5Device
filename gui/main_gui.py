# -*- encoding: utf-8 -*-
"""
@File    : main_gui.py
@Time    : 2021/9/26 11:45
@Author  : Coco
"""
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QGridLayout, QMainWindow, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = MainWidget()
        self.setWindowTitle("KEYSIGHT   E5080B")
        self.setFixedSize(1200, 768)
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

        self.vl_right = QVBoxLayout()
        self.vl_right.addWidget(self.plot_setting)
        self.vl_right.addWidget(self.global_setting)

        self.hl_main.addLayout(self.vl_left)
        self.hl_main.addLayout(self.vl_right)


class PlotSetting(QWidget):
    """   Function: 画图的参数设置，包括每个window的参数   """
    def __init__(self):
        super(PlotSetting, self).__init__()
        self._setupUI()

    def _setupUI(self):
        # 每个图形的参数设置采用网格布局
        self.gl_plot_setting = QGridLayout(self)

        # window 选择栏
        self.lb_window = QLabel("Window:")
        self.cb_window = QComboBox()
        self.window_list = ['1', '2', '3', '4']
        self.cb_window.addItems(self.window_list)
        # 测量参数选择栏
        self.lb_measure = QLabel("Measure:")
        self.cb_measure = QComboBox()
        self.measure_list = ['S11', 'S21', 'S12', 'S22']
        self.cb_measure.addItems(self.measure_list)
        # 属性选择栏
        self.lb_format = QLabel("Format:")
        self.cb_format = QComboBox()
        self.format_list = ['MLINear', 'MLOGarithmic', 'PHASe', 'POLar', 'SMITh', 'SWR', 'REAL', 'IMAGinary', 'GDELay',
                            'UPHase', 'PPHase']
        self.cb_format.addItems(self.format_list)
        # 保存设置按钮
        self.pb_save_setting = QPushButton("保存设置")

        # 控件添加到网格布局中
        self.gl_plot_setting.addWidget(self.lb_window, 0, 0)
        self.gl_plot_setting.addWidget(self.cb_window, 0, 1)
        self.gl_plot_setting.addWidget(self.lb_measure, 1, 0)
        self.gl_plot_setting.addWidget(self.cb_measure, 1, 1)
        self.gl_plot_setting.addWidget(self.lb_format, 2, 0)
        self.gl_plot_setting.addWidget(self.cb_format, 2, 1)
        self.gl_plot_setting.addWidget(self.pb_save_setting, 3, 1)


class GlobalSetting(QWidget):
    """   Function: 全局的参数设置，包括所有window的频率、点数等参数设置   """
    def __init__(self):
        super(GlobalSetting, self).__init__()
        self._setupUI()

    def _setupUI(self):
        self.gl_global_setting = QGridLayout(self)


class PlotArea(QWidget):
    """   Function: 画图区域设计   """
    def __init__(self):
        super(PlotArea, self).__init__()
        self._setupUI()

    def _setupUI(self):
        pass


class TableArea(QWidget):
    """   Function: 表格区域设计   """
    def __init__(self):
        super(TableArea, self).__init__()
        self._setupUI()

    def _setupUI(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
