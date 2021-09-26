# -*- encoding: utf-8 -*-
"""
@File    : visa_driver.py
@Time    : 2021/9/26 13:58
@Author  : Coco
"""
import time

import pyvisa


class Device:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource('USB0::0x2A8D::0x7901::MY59101311::0::INSTR')
        self.inst.timeout = 10000
        self.set_external_mode()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Device, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def set_external_mode(self):
        self.inst.write('TRIG:SOUR EXT')

    def set_internal_mode(self):
        self.inst.write("TRIG:SOUR IMM")

    def create_window(self, num, format_attr):
        self.inst.write('display:window{}:state on'.format(num))
        self.inst.write(':CALCulate{}:PARameter:COUNt 1'.format(num))
        self.set_internal_mode()
        self.single_sweep(num)
        # self.set_format_attr(num, format_attr)

    def set_format_attr(self, window_num, attr_type):
        self.inst.write('calculate:measure{}:format {}'.format(window_num, attr_type))

    def set_trace(self, window_num):
        self.inst.write(':CALCulate{}:PARameter:COUNt 1'.format(window_num))
        time.sleep(2)
        # self.set_Meas(window_num, 'S11')
        # self.inst.write('display:window{}:trace:state on'.format(window_num))
        self.single_sweep(window_num)

    def select_trace(self, window_num, trace_num):
        self.inst.write('display:window{}:trace{}:select'.format(window_num, trace_num))

    def query_trace_count(self, window_num):
        count = int(self.inst.query(f'display:window{window_num}:trace:NEXT?').strip('+')) - 1
        return count

    def preset(self):
        self.inst.write('SYST:PRES')

    def set_Meas(self, window_num, measure_mode):
        self.inst.write(':CALCulate:MEASure{}:PARameter {}'.format(window_num, measure_mode))

    def single_sweep(self, num):
        self.inst.write('sense{}:sweep:mode single'.format(num))

    def set_sweep_parameter(self, start_freq, end_freq, center_freq, sweep_points):
        self.inst.write('SENS:FREQ:STAR {}'.format(start_freq))
        self.inst.write('SENS:FREQ:STOP {}'.format(end_freq))
        self.inst.write('SENS:FREQ:CENT {}'.format(center_freq))
        self.inst.write('SENS:SWE:POIN {}'.format(sweep_points))


if __name__ == '__main__':
    my_device = Device()
    my_device.set_external_mode()
    my_device.create_window(3, 'polar')
    # my_device.set_format_attr(2, 'polar')
    # my_device.create_window(4, 'polar')
