#!/usr/bin/env python

import os


try:
    from sonic_platform_base.psu_base import PsuBase
    from sonic_platform.led_control import LEDControl
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")


class Psu(PsuBase):
    """PDDF Platform-Specific PSU class"""
    sys_fs_base = "/sys/bus/i2c/devices"
    
    PLATFORM_PSU_CAPACITY = 1100

    def __init__(self, index):
        self.__sys_fs_psu = [ os.path.join(Psu.sys_fs_base, "40-0058"),
                              os.path.join(Psu.sys_fs_base, "41-0058") ][index]
        self.__index = index
        self._fan_list = [ None ]
        self._thermal_list = [ None ]
        self.__led_control = LEDControl()
        PsuBase.__init__(self)

    def __read_sysfs(self, fname):
        with open(os.path.join(self.__sys_fs_psu, fname), "r") as sysfs_fd:
            return sysfs_fd.read()[:-1]

    def get_name(self):
        return "%s-%d" % (self.__read_sysfs("name"), self.__index)

    def get_presence(self):
        '''Check if the apporpriate sysfs entry exists'''
        return os.path.exists(self.__sys_fs_psu)

    def get_model(self):
        return self.__read_sysfs("psu_mfr_model")

    def get_serial(self):
        return self.__read_sysfs("psu_mfr_serial")

    def get_voltage(self):
        return float(self.__read_sysfs("in1_input")) / 1000.0

    def get_current(self):
        return float(self.__read_sysfs("curr1_input")) / 1000.0
        
    def get_power(self):
        return float(self.__read_sysfs("power1_input")) / 1000000.0
        
    def get_powergood_status(self):
        '''For the ag9032v1 there is no flag for this. Use the voltages
        to decide if the status is good'''
        voltage_in = self.get_voltage()
        voltage_out = float(self.__read_sysfs("in2_input")) / 1000.0

        return voltage_in > 0.0 and voltage_out > 0.0

    def get_status_led(self):
        return self.__led_control.get_status("pwr%d" % (self.__index+1))

    def set_status_led(self, color):
        print("NOT IMPLEMENTED set_status_led", color)
        assert False
        
    def get_temperature(self):
        print("NOT IMPLEMENTED get_temperature")
        assert False
        
    def get_temperature_high_threshold(self):
        print("NOT IMPLEMENTED get_temperature_high_threshold")
        assert False
        
    def get_voltage_low_threshold(self):
        print("NOT IMPLEMENTED get_temperature_low_threshold")
        assert False
        
    def get_maximum_supplied_power(self):
        print("NOT IMPLEMENTED get_maximum_supplied_power")
        assert False
        
    def get_status_master_led(self):
        print("NOT IMPLEMENTED get_status_master_led")
        assert False

    def set_status_master_led(self, color):
        print("NOT IMPLEMENTED set_status_master_led", color)
        assert False
        
