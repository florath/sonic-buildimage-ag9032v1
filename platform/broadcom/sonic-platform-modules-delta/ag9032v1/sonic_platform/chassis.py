'''
sonic_platform Chassis implementation for ag9032v1
'''

try:
    from sonic_platform_base.chassis_base import ChassisBase
    from sonic_platform.psu import Psu
    from sonic_platform.led_control import LEDControl
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")


class Chassis(ChassisBase):

    def __init__(self):
        print("Chassis init for ag9032v1")
        ChassisBase.__init__(self)
        self.__led_control = LEDControl()
        self._psu_list = [ Psu(0), Psu(1) ]

    #def get_num_psus(self):
    #    '''The ag9032v1 has two PSUs'''
    #    return 2

    def initizalize_system_led(self):
        '''Nothing to initialize - apart from the i2c bus which is
        already initialized.'''
        return True

    def get_status_led(self):
        return self.__led_control.get_status("sys")

    def set_status_led(self, color):
        self.__led_control.set_status("sys", color)

    def get_serial(self):
        return "n/a"

    def get_model(self):
        return "ag9032"

    def get_revision(self):
        return "v1"
